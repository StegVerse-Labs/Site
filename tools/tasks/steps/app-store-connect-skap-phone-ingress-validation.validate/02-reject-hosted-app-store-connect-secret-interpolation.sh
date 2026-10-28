if grep -R -n -E 'secrets\.ASC_|\$\{\{[[:space:]]*secrets\.' \
  assets/stegos-apple stegos-apple-credential.html; then
  echo '::error::Hosted App Store Connect secret interpolation detected'
  exit 1
fi
