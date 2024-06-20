import hashlib
input_pwd = "123"
double_pwd = "123"
for i in range(100):
    input_password = hashlib.sha256(str(input_pwd).encode()).hexdigest()
    stored_password = hashlib.sha256(str(double_pwd).encode()).hexdigest()
    print(f'input_password : {input_password}')
    print(f'stored_password: {stored_password}')
    print('-'*80)
