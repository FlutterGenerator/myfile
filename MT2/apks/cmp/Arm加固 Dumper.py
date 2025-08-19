# private static byte[] encrypt(byte[] bArr) {
        # byte[] bArr2 = new byte[bArr.length];
        # for (int i = 0; i < bArr.length; i++) {
            # bArr2[i] = (byte) (bArr[i] ^ 255);
        # }
        # return bArr2;
    # }
    
# Dev @aantik_mods

import zipfile
import os

def xor_decrypt(encrypted_data, key=0xFF):


    decrypted_data = bytearray()
    
    
    for byte in encrypted_data:
    
    
        decrypted_data.append(byte ^ key)
        
        
    return bytes(decrypted_data)

def extract_encrypted_data(zip_file_path, dex_file_name):


    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:  # only read file ok
    
    
        file_list = zip_ref.namelist()
        
        classes_files = [file for file in file_list if file.startswith('assets/classes') and file.endswith('.dex')]
        
        if not os.path.exists(out_dir):
        
        
            os.makedirs(out_dir)
        
        for classes_file in classes_files:
        
        
            encrypted_data = zip_ref.read(classes_file)
            
            
            decrypted_data = xor_decrypt(encrypted_data)
            
            
            output_file_path = os.path.join(out_dir, os.path.basename(classes_file))
            
            with open(output_file_path, 'wb') as output_file:
            
            
                output_file.write(decrypted_data)
            
            # print my logs ok dumping hope you enjoy my Video 🥲
            print(f"Dump {classes_file} Save Path => '{output_file_path}'")

def decrypt_all_classes(zip_file_path, out_dir):

    extract_encrypted_data(zip_file_path, out_dir)




zip_file_path = 'Arm加固.apk'


out_dir = 'out_dir'


decrypt_all_classes(zip_file_path, out_dir)
