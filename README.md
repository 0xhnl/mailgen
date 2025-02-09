# Email Splitter for Gophish Campaigns

This Python script helps you split a large list of emails into smaller CSV files, which can then be uploaded to Gophish for phishing campaign management. It ensures that your email lists are properly formatted and divided into manageable chunks, making it easier to handle large-scale campaigns.

## Features
- Chunked CSV Generation : Automatically splits a list of emails into smaller CSV files based on a specified chunk size.
- Gophish-Compatible Format : Generates CSV files with columns: First Name, Last Name, Email, and Position.
- Dynamic File Naming : Outputs files named G01.csv, G02.csv, ..., ensuring easy identification.
- Handles Edge Cases : Properly handles leftover emails (e.g., if the total number of emails isn't divisible by the chunk size).
- Customizable Chunk Size : Allows you to specify the number of emails per CSV file.

## Installations

- Clone this repository:

```bash
git clone https://github.com/0xhnl/mailgen.git
cd mailgen
```

## Command-Line Arguments

- Run the script with the following arguments:

```bash
➜  mailgen python3 mailgen.py 
usage: mailgen.py [-h] -i INPUT -c CHUNK
mailgen.py: error: the following arguments are required: -i/--input, -c/--chunk
```

- Create a text file (emails.txt) containing one email per line:

```txt
test@gmail.com
test1@gmail.com
test2@gmail.com
...
```

- Split Emails into Chunks of 100:

```bash
➜  mailgen python3 mailgen.py -i emails.txt -c 100
Created output/G01.csv with 100 emails.
Created output/G02.csv with 100 emails.
Created output/G03.csv with 100 emails.
Created output/G04.csv with 100 emails.
Created output/G05.csv with 100 emails.
Created output/G06.csv with 100 emails.
Created output/G07.csv with 100 emails.
Created output/G08.csv with 100 emails.
Created output/G09.csv with 100 emails.
Created output/G10.csv with 100 emails.
Created output/G11.csv with 100 emails.
Created output/G12.csv with 100 emails.
Created output/G13.csv with 100 emails.
Created output/G14.csv with 100 emails.
Created output/G15.csv with 100 emails.
Created output/G16.csv with 100 emails.
Created output/G17.csv with 100 emails.
Created output/G18.csv with 100 emails.
Created output/G19.csv with 100 emails.
Created output/G20.csv with 94 emails.
Total 20 CSV files created in 'output' directory.

➜  mailgen ls output 
G01.csv G03.csv G05.csv G07.csv G09.csv G11.csv G13.csv G15.csv G17.csv G19.csv
G02.csv G04.csv G06.csv G08.csv G10.csv G12.csv G14.csv G16.csv G18.csv G20.csv
```

- After that, you can send those csv files to the gophish host. Both support single csv file or folder which contain csv files.

```bash
➜  mailgen python3 gpcreate.py -H <gophish-host> -k <gophish-api-key> -ff output      
Successfully uploaded group G14
Successfully uploaded group G15
Successfully uploaded group G01
➜  mailgen python3 gpcreate.py -H <gophish-host> -k <gophish-api-key> -f output/G14.csv      
Successfully uploaded group G14
```

- Finally, you can launch the phishing campaign with specific name.

```bash
➜  mailgen python3 send.py \ 
    -l "test landing" \
    -t "test landing" \
    -u http://123.123.123.123 \
    -p test \
    -g test \
    -c test \
    -now
[+] Launching campaign immediately at: 2025-02-09T05:52:49Z
[+] Successfully created campaign: test
```

## Note

- For an input file with 1233 emails and a chunk size of 100:
  - output/G01.csv to output/G12.csv contain 100 emails each.
  - output/G13.csv contains the remaining 33 emails.
- For an input file with 1260 emails and a chunk size of 100:
  - output/G01.csv to output/G12.csv contain 100 emails each.
  - output/G13.csv contains the remaining 60 emails.

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## Support

If you find this tool helpful, please consider giving it a ⭐️ on GitHub. For questions or feedback, open an issue in the repository.
