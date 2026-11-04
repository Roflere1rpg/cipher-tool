def aes_encrypt(text: str, key: str) -> str:
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
    text_bytes = text.encode('utf-8')
    padded_text = text_bytes.ljust((len(text_bytes) + 15) // 16 * 16, b'\0')
    
    result = []
    for i in range(0, len(padded_text), 16):
        block = padded_text[i:i+16]
        # Упрощенное шифрование: XOR блока с ключом
        encrypted_block = bytes([b ^ k for b, k in zip(block, key_bytes)])
        result.append(encrypted_block)
    
    return " ".join([b.hex() for b in result])