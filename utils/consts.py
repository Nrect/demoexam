import envv
SERVER_NAME = envv.server_name
DATABASE_NAME = envv.database_name
USER_NAME = envv.user_name
USER_PASSWORD = envv.user_password

TABLE_MANUFACTURE = 'Manufacturer'
TABLE_PRODUCT = 'Product'
TABLE_PRODUCT_SALE = 'ProductSale'

server_name = 'DESKTOP-T26UFOU\SQLEXPRESS'
database_name = 'beauty_salon_user6'
user_name = ''
user_password = ''

connection_string = f'DRIVER={{SQL Server}};' \
                    f'SERVER={server_name};' \
                    f'UID={user_name};' \
                    f'PWD={user_password};' \
                    f'DATABASE={database_name};'

