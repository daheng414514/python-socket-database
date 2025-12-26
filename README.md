# Python Socket Database

A simple client–server database application built using Python sockets.  
The server listens for TCP connections, processes structured requests, and stores customer records in a text-based database.

This project was built as a learning exercise to explore TCP socket programming, basic protocol design, and server-side validation in Python.

---

## Technologies Used

- Python 3
- `socket`
- `socketserver`
- Regular expressions (`re`)
- Threading (for controlled server shutdown)

---

## Project Structure

```
python-socket-database/
├── server.py        # TCP server implementation
├── client.py        # Client-side menu interface
├── data.txt         # Initial database file
├── data_out.txt     # Updated database output
└── README.md
```

---

## Usage / How to Run

### Requirements
- Python 3.9+
- No external libraries required (standard library only)

### Step 1: Start the Server
- Open a terminal in the project root directory and run:
```bash
python server.py
```
  You should see:
```bash
Server is running... listening on localhost:9999
```
  
### Step 2: Run the Client
- Open another terminal in the same directory and run:
```bash
python client.py
```
  This will display the interactive menu.
  
### Step 3: Using the Application
- The client provides a menu-driven interface:
  
  1. Find Customer
  2. Add Customer
  3. Delete Customer
  4. Update Customer Age
  5. Update Customer Address
  6. Update Customer Phone
  7. Print Report
  8. Update File and Exit

-	Input is validated on both client and server sides
-	The server processes one request per connection
-	Data is stored in memory during runtime

### Step 4: Saving and Shutting Down
- To save the database and shut down the server:
  1.	Choose option 8 in the client
  2.	The server writes data to data_out.txt
  3.	The server shuts down gracefully 
- After shutdown, the server must be restarted manually:
```bash
python server.py
```

### Notes
- The server accepts one client connection at a time (intentional design)
- Requests are delimited using a newline (`\n`) as the protocol terminator
- Maximum request size is limited to prevent malformed input
- All communication uses TCP sockets

---

## Features

- TCP client–server architecture using Python sockets
- Menu-driven client interface
- Supports CRUD-style operations:
    - Create (Add Customer)
    - Read (Find Customer, Print Report)
    - Update (Update Age, Address, Phone)
    - Delete (Remove Customer)
- Custom text-based protocol using `|` separators and `\n` as a message delimiter
- Input validation on both client and server sides
- Case-insensitive customer name matching
- In-memory data storage with persistence to a text file on shutdown
- Graceful server shutdown triggered by client command
- Request size limits, timeout handling, and protection against malformed input

---

## Design Decisions

- The server is intentionally designed to handle one client session per run
- A simple text-based protocol is used for clarity and learning purposes
- Messages are delimited using a newline (`\n`) to clearly define request boundaries
- Customer names are treated as case-insensitive for usability
- Data is stored in memory during runtime and written to file only on shutdown
- A menu-driven client interface is used to simplify user interaction

---

## Limitations

- This project is not intended for production use
- Only one client should connect to the server at a time
- Data persistence relies on plain text files rather than a real database
- No authentication or encryption is implemented
- The server must be restarted manually after shutdown
