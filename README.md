# Online Group Chatting Application

This online group chatting Python application utilizes TCP and UDP connection to allow multiple concurrent client connections. The commands are shown below.

• connect : The client connects to the CRDS on the CRDP. Once connected, the
client can issue the CRDS commands discussed above, i.e., getdir, makeroom
and deleteroom. The CRDS responds as discussed previously. You should use a
different command line prompt to show that you are connected to the CRDS.<br>
• bye : This closes the client-to-CRDS connection, returning the user to the main command prompt.<br>
• name <chat name> : This command sets the name that is used by the client when
chatting, e.g., name Mel. All chat messages will be automatically prefixed with this
name, e.g., “Mel: Good morning!”.<br>
• chat <chat room name> : The client enters “chat mode” using the multicast
address/port for the associated chat room. You should change the command line prompt
so that it is clear when chat mode has been entered.<br>
• getdir : The server returns a copy of the current chat room directory (CRD).
Each entry in the directory includes the chat room name, multicast IP adddress
and port.<br>
• makeroom \<chat room name> \<address> \<port> : The server creates a chat room directory (CRD) entry that includes the above information. Note
that \<address> is an IP multicast address used by the clients for chat messages
(Use the administratively scoped IP multicast range:
239.0.0.0 to 239.255.255.255).
The CRDS should check that the new address/port combination is not currently in
the directory.<br>
• deleteroom \<chat room name> : The CRDS removes the chat room entry
from the CRD.

### To use:
Run both server and client Python scripts and run the commands when prompted. 
