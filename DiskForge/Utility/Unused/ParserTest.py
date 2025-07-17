import re

sample_texts = [
    "Nov 23 15:24:46 niclas-VirtualBox NetworkManager[498]: <info> [1700749486.3199] Read config: /etc/NetworkManager/NetworkManager.conf (lib: 10-dns-resolved.conf, 20-connectivity-ubuntu.conf, no-mac-addr-change.conf) (run: 10-globally-managed-devices.conf) (etc: default-wifi-powersave-on.conf)",
    # Add more sample texts as needed
]

# Define the regular expression pattern
epoch_time_pattern = re.compile(r'\[([\d.]+)\]')

# Loop through each sample text
for sample_text in sample_texts:
    # Search for the epoch time pattern in the sample text
    match = epoch_time_pattern.search(sample_text)

    # Check if a match is found and print the result
    if match:
        extracted_epoch_time = match.group(1)
        print("Extracted epoch time:", extracted_epoch_time)
    else:
        print("Epoch time not found in the given text.")
