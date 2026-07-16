
---

**2. Create `SECURITY.md`**
Copy this into a file called `SECURITY.md` in your root folder:

```markdown
# Security Policy

## Supported Versions

Currently, only the latest version of this project is actively supported with security updates.

| Version | Supported |
| :--- | :--- |
| 1.0.0 (Latest) | ✅ |

---

## Reporting a Vulnerability

While this project does not handle sensitive patient data (PHI) and runs entirely offline, I take the security and ethical use of healthcare tools seriously. If you discover a vulnerability, please **do not** open a public GitHub issue.

Instead, please send an email to: **[yujass73@gmail.com]** with the subject line: `[Security] PFT AI Companion`.

I will respond within 48 hours and work with you to resolve the issue promptly.

---

## Security Considerations for This Project

- **Offline-First:** This application runs entirely on your local machine. No data is transmitted over the internet.
- **No Data Storage:** Patient recordings and scores are not stored or logged beyond the current session in memory.
- **Clinical Disclaimer:** This application is explicitly marked as **educational and decision-support only**. It is **not** a medical device and does **not** replace clinical judgment (as noted in the main [README](README.md)).
- **Dependency Management:** Regularly update `requirements.txt` to patch known vulnerabilities in dependencies (`pyttsx3`, `gradio`, etc.).

---

## Responsible Disclosure Policy

If you report a vulnerability in good faith, I will:
- Investigate and confirm the issue.
- Not take legal action against you.
- Credit you for the discovery (if you wish).

---

**Last Updated:** July 2026
