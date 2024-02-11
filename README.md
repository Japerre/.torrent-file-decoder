# .torrent-file-decoder

On my journey of learning about the bittorrent protocol, I came accross the .torrent file format. .torrent files are bencoded dictionaries. To learn more about these .torrent files and bencoding in general, I wrote a simple decoder for .torrent files.

## it includes functionality to
1) decode a .torrent meta file and put it's contents into a json file
2) check the integrity of a downloaded torrent by comparing its hash to the hash in the .torrent file

## Works with
1) .torrent files hashed by SHA1 algorithm
2) .torrent files for downloading a single file (such as a Linux ISO)

## try it out yourself

```shell
git clone https://github.com/Japerre/.torrent-file-decoder.git
cd .torrent-file-decoder
```
- download Linux ISO file such as Debian12.5.0 with a torrent client such as QBittorrent ==> https://cdimage.debian.org/debian-cd/current/amd64/bt-cd/debian-12.5.0-amd64-netinst.iso.torrent
- put ISO file in downloaded_files folder
-  edit paths in bparser.py
 
```shell
python bparser.py
```
