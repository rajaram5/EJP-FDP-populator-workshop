import chevron

class Utils:

    def get_catalog_body(self, catalog):
        catalog_body = None
        with open('../templates/catalog.mustache', 'r') as f:
            catalog_body = chevron.render(f, {'title': catalog.TITLE, 'description': catalog.DESCRIPTION,
                                              'fdp_url': catalog.FDP_URL})
        return catalog_body

    def get_resource_body(self, resource, catalog_url):

        resource_body = None

        keyword_str = ""
        for keyword in resource.KEYWORDS:
            keyword_str = keyword_str + ' "' + keyword + '",'
        keyword_str = keyword_str[:-1]

        theme_str = ""
        for theme in resource.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        with open('../templates/resource.mustache', 'r') as f:
            resource_body = chevron.render(f, {'resourceType': resource.TYPE, 'title': resource.TITLE,
                                               'description': resource.DESCRIPTION, 'catalog_url': catalog_url,
                                                'keyword': keyword_str, 'theme': theme_str,
                                               'publisher': resource.PUBLISHER_NAME})
        return resource_body