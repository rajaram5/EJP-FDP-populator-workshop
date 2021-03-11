import FdpPopulator

fdp_url = "http://localhost"
#fdp_url = "http://ejprd.fair-dtls.surf-hosted.nl:8094"
fdp_admin_user = "albert.einstein@example.com"
fdp_admin_password = "password"
input_file = "/home/rajaram/Downloads/FDP-template.xlsx"
FdpPopulator.FdpPopulator(fdp_url, fdp_admin_user, fdp_admin_password, input_file)