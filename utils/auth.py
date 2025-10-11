import pyotp

# import qrcode

chave_mestre = "V6V4DGNYW3NB5MFROLMZT64WD3NBBST6"

codigo = pyotp.TOTP(chave_mestre)

# link = pyotp.TOTP(chave_mestre).provisioning_uri(name="aluno", issuer_name="HelpDesk_Etec")

# meu_qrcode = qrcode.make(link)
# meu_qrcode.save("../assets/qrcode.png")
