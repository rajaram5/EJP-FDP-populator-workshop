import Resource
import Catalog
import FDPClient
import Utils
import pandas

class FdpPopulator:

    FDP_URL = None
    FDP_CLIENT = None
    INPUT_FILE = None
    UTILS = Utils.Utils()
    IS_ROW_1_HEADER = True
    CATALOGS = {}
    GUIDELINES = []
    DATA_SHEET_NAME = "resources"

    def __init__(self, fdp_url, fdp_admin_user, fdp_admin_user_password, input_file):
        self.FDP_URL = fdp_url
        self.FDP_CLIENT = FDPClient.FDPClient(fdp_url, fdp_admin_user, fdp_admin_user_password)
        self.INPUT_FILE = input_file
        self.__populate_fdp__()

    def __populate_fdp__(self):

        catalogs = {}
        resources = []

        excel_data_df = pandas.read_excel(self.INPUT_FILE, sheet_name=self.DATA_SHEET_NAME)

        for i in excel_data_df.index:
            resource_type = self.__clean_string__(excel_data_df['Resource type'][i])
            if resource_type:
                catalog = None
                if resource_type not in self.CATALOGS:
                    catalog_description = resource_type
                    catalog = Catalog.Catalog(resource_type, catalog_description, self.FDP_URL)
                    catalogs[resource_type] = catalog
                else:
                    catalog = catalogs[resource_type]

                resource_name = self.__clean_string__(excel_data_df['Name'][i])
                resource_description = self.__clean_string__(excel_data_df['Description'][i])
                # if description is empty please use title
                if not resource_description:
                    resource_description = resource_name

                resource_keyword = []
                for keyword in excel_data_df['Keyword'][i].split(";"):
                    keyword = self.__clean_string__(keyword)
                    resource_keyword.append(keyword)
                resource_theme = []
                for theme in excel_data_df['Theme'][i].split(";"):
                    theme = self.__clean_string__(theme)
                    resource_theme.append(theme)
                resource_publisher = self.__clean_string__(excel_data_df['Publisher name'][i])
                resource_type_url = None
                if resource_type == "Biobank":
                    resource_theme.append("http://www.wikidata.org/entity/Q864217")
                    resource_keyword.append("Biobank")
                    resource_type = "http://purl.org/biosemantics-lumc/ontologies/dcat-extension/Biobank"

                if resource_type == "Patient registry":
                    resource_theme.append("http://www.wikidata.org/entity/Q5282128")
                    resource_keyword.append("Patient registry")
                    resource_type = "http://purl.org/biosemantics-lumc/ontologies/dcat-extension/PatientRegistry"

                if not resource_publisher:
                    resource_publisher = "EJP RD"

                resource = Resource.Resource(resource_type, resource_name, resource_description, resource_publisher,
                                             resource_keyword, resource_theme, catalog)
                resources.append(resource)


        catalog_urls = {}
        for catalog_name in catalogs.keys():
            catalog = catalogs[catalog_name]
            catalog_body = self.UTILS.get_catalog_body(catalog)
            catalog_url = self.FDP_CLIENT.fdp_create_metadata(catalog_body, "catalog")
            catalog_urls[catalog_name] = catalog_url


        for resource in resources:
            catalog_url = catalog_urls[resource.CATALOG.TITLE]
            resource_body = self.UTILS.get_resource_body(resource, catalog_url)
            print(resource_body)

            if resource.TYPE == "http://purl.org/biosemantics-lumc/ontologies/dcat-extension/Biobank":
                resource_url = self.FDP_CLIENT.fdp_create_metadata(resource_body, "biobank")
            elif resource.TYPE == "http://purl.org/biosemantics-lumc/ontologies/dcat-extension/PatientRegistry":
                resource_url = self.FDP_CLIENT.fdp_create_metadata(resource_body, "patientRegistry")

    def __clean_string__(self, input):
        input = input.strip()
        return input

fdp_url = "http://localhost"
fdp_admin_user = "albert.einstein@example.com"
fdp_admin_password = "password"
input_file = "/home/rajaram/Downloads/FDP-template.xlsx"
test = FdpPopulator(fdp_url, fdp_admin_user, fdp_admin_password, input_file)