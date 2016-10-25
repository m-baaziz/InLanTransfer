# InLanTransfer
Python App designed to transfer files through a local network, using :
  - threading
  - socket
  - Tkinter
  
## How it works

First the main app will create two threads :
  - the broadcaster
  - the listener

The broadcaster will ping every node on the network so that they can update their user list.

The listener will listen to every incoming message and carry out the corresponding action.

When a user clicks on a User Button, the main app produces a File Dialog. As soon as the user chooses the file to send, App sends a request to the remote node. 

If the remote node accepts, the file transfer proceeds : the file is sent chunk by chunk, each one has to be acknowledged before the next one is sent.

## Communication Protocol

- PING :

  datagramme =  $NAME:PING  -> broadcasting message
- REQUEST

  datagramme = $NAME:REQUEST:$FILENAME:$FILESIZE  -> ask the node to accept the file
- ACCEPT :

  datagramme = $NAME:ACCEPT:$FILENAME -> accept the request (the file transfer)
- REFUSE :

  datagramme = $NAME:REFUSE:$FILENAME -> refuse the request (the file transfer)
- DATA :

  datagramme = $NAME:DATA:$FILENAME:$FILESIZE:$DATASIZE:$DATA -> send a data packet
- ACK :

  datagramme = $NAME:ACK:$FILENAME:$FILESIZE:$DATASIZE -> acknowledge having received $DATASIZE bytes from the start of the exchange (the sender will continue from there)
- EOF :

  datagramme = $NAME:EOF:$FILENAME -> end of file, transmission over
- END :

  datagramme = $NAME:END  -> the user $NAME disconected

## Demo

<center>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=O6nVn01DYBQ" target="_blank"><img src="http://img.youtube.com/vi/O6nVn01DYBQ/0.jpg" alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
</center>
