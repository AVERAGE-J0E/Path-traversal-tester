## 📌 Overview
This basic script is a **Path Traversal Brute Force Tester** designed to test web applications for path traversal vulnerabilities. It attempts to access restricted files by iterating through directory levels using `../` traversal patterns.

## 🔧 Command-Line Arguments

```sh
python path_traversal.py -t <TARGET_URL> [options]
```

### **Required Arguments**
| Argument | Description |
|----------|-------------|
| `-t, --target` | The target URL with the vulnerable parameter (e.g., `http://test.com/download?path=`) |

### **Optional Arguments**
| Argument | Description | Default |
|----------|-------------|---------|
| `-d, --depth` | Maximum traversal depth (number of `../` levels) | `10` |
| `-f, --file` | File path to attempt access (exclude first `/`) | `etc/passwd` |
| `-e, --expected-string` | String expected in response (indicating success) | `root:x:` |
| `-H, --header` | Custom headers (format: `Key: Value`). Can be used multiple times. | `None` |

### **Example Usage**
1. **Basic Test**
   ```sh
   python path_traversal.py -t "http://example.com/download?path="
   ```
2. **Increasing Traversal Depth**
   ```sh
   python path_traversal.py -t "http://example.com/download?path=" -d 20
   ```
3. **Looking for a Different File**
   ```sh
   python path_traversal.py -t "http://example.com/download?path=" -f "var/www/html/config.php"
   ```
4. **Using Custom Headers**
   ```sh
   python path_traversal.py -t "http://example.com/download?path=" -H "User-Agent: Mozilla/5.0" -H "Authorization: Bearer TOKEN"
   ```

## ⚠️ Disclaimer
This tool is intended for educational purposes and **authorized security testing only**. Unauthorized use against systems without explicit permission is illegal.

