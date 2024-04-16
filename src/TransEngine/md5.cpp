//
// Created by pzy123 on 4/16/2024.
//

// Utility function to convert bytes to a hex string
#include "TransEngine/md5.h"
std::string bytesToHexString(const BYTE* bytes, DWORD length) {
    std::string hexStr;
    char buffer[3];
    for (DWORD i = 0; i < length; ++i) {
        sprintf_s(buffer, sizeof(buffer), "%02x", bytes[i]);
        hexStr.append(buffer);
    }
    return hexStr;
}

// Function to compute MD5 hash of a string
std::string computeMD5(const std::string& input) {
    HCRYPTPROV hProv = 0;
    HCRYPTHASH hHash = 0;
    BYTE hash[MD5LEN]; // MD5 hash length is 16 bytes
    DWORD hashLen = MD5LEN;
    std::string result;

    // Acquire a cryptographic provider context
    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
        std::cerr << "CryptAcquireContext failed: " << GetLastError() << std::endl;
        return result;
    }

    // Create a new hash object
    if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash)) {
        std::cerr << "CryptCreateHash failed: " << GetLastError() << std::endl;
        CryptReleaseContext(hProv, 0);
        return result;
    }

    // Compute the cryptographic hash of the buffer
    if (!CryptHashData(hHash, reinterpret_cast<const BYTE*>(input.c_str()), input.length(), 0)) {
        std::cerr << "CryptHashData failed: " << GetLastError() << std::endl;
    } else {
        // Retrieve the hash value
        if (CryptGetHashParam(hHash, HP_HASHVAL, hash, &hashLen, 0)) {
            result = bytesToHexString(hash, hashLen);
        } else {
            std::cerr << "CryptGetHashParam failed: " << GetLastError() << std::endl;
        }
    }

    // Clean up
    if (hHash) CryptDestroyHash(hHash);
    if (hProv) CryptReleaseContext(hProv, 0);

    return result;
}

int main() {
    std::string input = std::string("20240303001980861Hello, world!c8MMKDWGKWomS_co4V5M");
    std::string md5Hash = computeMD5(input);
    std::cout << "MD5 Hash of '" << input << "': " << md5Hash << std::endl;
    return 0;
}
