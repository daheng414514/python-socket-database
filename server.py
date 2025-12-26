import socketserver
import socket
import re
import threading

class server(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(3)
        try:
            raw = b""
            while b"\n" not in raw:
                chunk_part = self.request.recv(256)
                if not chunk_part:
                    self.request.sendall(b"Incomplete request (connection closed before delimiter).")
                    return
                raw += chunk_part
                if len(raw) > 512:
                    self.request.sendall(b"Input too long...")
                    return
        
            msg = raw.split(b"\n", 1)[0].decode('utf-8', errors="replace").strip()
            print("\nMessage from client:", msg)
            parts = [p.strip() for p in msg.split("|")]

            if not parts or not parts[0]:
                self.request.sendall(b"Empty message received...")
                return


            if parts[0] == "1":
                if len(parts) != 2:
                    self.request.sendall(b"Input formate dismatch")
                    return

                index = -1
                for i in range(len(db)):
                    if db[i]["name"].lower() == parts[1].lower():
                        index = i
                if index == -1:
                    reply = f"{parts[1]} is not found in database"
                else:
                    info = db[index]
                    reply = info["name"] + "|" + info["age"] + "|" + info["address"] + "|" + info["phone#"]
                self.request.sendall(reply.encode("utf-8"))
                return
                    
            elif parts[0] == "2":
                if len(parts) != 5:
                    self.request.sendall(b"Input formate dismatch.")
                    return

                phonenumber = re.compile(r"^(394|426|901|514)-\d{4}$")
                parts.pop(0)
                reply=""
                if any(data["name"].lower() == parts[0].lower() for data in db):
                    reply = f"{parts[0]} already stored in the database"
                else:
                    try:
                        if not parts[0]:
                            raise ValueError(f"DB read error. Adding skipped [null key field]: {parts}")
                        if parts[1]:
                            if not parts[1].isdigit():
                                raise ValueError(f"DB read error. Adding skipped [invalid age formate]: {parts[1]}")
                            if(int(parts[1]) < 1 or int(parts[1]) > 120):
                                raise ValueError(f"DB read error. Adding skipped [invalid age field]: {parts[1]}")
                        if parts[3] and not phonenumber.match(parts[3]):
                            raise ValueError(f"DB read error. Adding skipped [invalid phone field]: {parts[3]}")
                    except ValueError as e:
                        reply = str(e)
                        self.request.sendall(reply.encode("utf-8"))
                        return                    

                    db.append({
                        "name": parts[0],
                        "age" : parts[1],
                        "address": parts[2],
                        "phone#" : parts[3]
                    })
                    reply = f"{msg} added to the database"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "3":
                if len(parts) != 2:
                    self.request.sendall(b"Input formate dismatch")
                    return
                reply = ""
                if not parts[1]:
                    reply = "Customer name is empty."
                else:
                    for i in range(len(db)):
                        if db[i]["name"].lower() == parts[1].lower():
                            db.pop(i)
                            reply = f"{parts[1]} deleted from the database"
                            break
                        if i == len(db)-1:
                            reply = f"{parts[1]} is not found in the database"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "4":
                if len(parts) != 3:
                    self.request.sendall(b"Input formate dismatch")
                    return
                parts.pop(0)

                index = -1
                for i in range(len(db)):
                    if db[i]["name"].lower() == parts[0].lower():
                        index = i
                if index == -1:
                    reply = f"{parts[0]} is not found in database"
                else:
                    try:
                        if parts[1]:
                            if not parts[1].isdigit():
                                raise ValueError(f"DB read error. Update skipped [invalid age formate]: {parts}")
                            if(int(parts[1]) < 1 or int(parts[1]) > 120):
                                raise ValueError(f"DB read error. Update skipped [invalid age field]: {parts[1]}")
                    except ValueError as e:
                        reply = str(e)
                        self.request.sendall(reply.encode("utf-8"))
                        return 
                    db[index]["age"] = parts[1]
                    reply = f"{parts[0]}'s age is updated to the database"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "5":
                if len(parts) != 3:
                    self.request.sendall(b"Input formate dismatch")
                    return
                parts.pop(0)

                index = -1
                for i in range(len(db)):
                    if db[i]["name"].lower() == parts[0].lower():
                        index = i
                if index == -1:
                    reply = f"{parts[0]} is not found in database"
                else:
                    db[index]["address"] = parts[1]
                    reply = f"{parts[0]}'s address is updated to the database"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "6":
                if len(parts) != 3:
                    self.request.sendall(b"Input formate dismatch")
                    return
                parts.pop(0)
                phonenumber = re.compile(r"^(394|426|901|514)-\d{4}$")
                index = -1
                for i in range(len(db)):
                    if db[i]["name"].lower() == parts[0].lower():
                        index = i
                if index == -1:
                    reply = f"{parts[0]} is not found in database"
                else:
                    try:
                        if parts[1] and not phonenumber.match(parts[1]):
                            raise ValueError(f"DB read error. Adding skipped [invalid phone field]: {parts[1]}")
                    except ValueError as e:
                        reply = str(e)
                        self.request.sendall(reply.encode("utf-8"))
                        return 
                    db[index]["phone#"] = parts[1]
                    reply = f"{parts[0]}'s phone number is updated to the database"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "7":
                db.sort(key=lambda a: a["name"].lower())
                reply = f"""
                \n++    
                \n++  DB Report
                \n++
                \nName {'':<10} {'Age':<15}{'address':<30}Phone Number
                \n-------------------------------------------------------------------------\n"""
                for i in range(len(db)):
                    reply += f"{db[i]['name'][:10]:<15} {db[i]['age']:<15}{db[i]['address'][:21]:<30}{db[i]['phone#']}\n"
                self.request.sendall(reply.encode("utf-8"))
                return

            elif parts[0] == "8":
                write_file("data_out.txt")
                reply = "File update successful. Server shutting down...\n"
                self.request.sendall(reply.encode("utf-8"))
                print("Server is closing connection.")
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return

            else:
                reply = "invalid choice...\n"
                self.request.sendall(reply.encode("utf-8"))
                return
        
        except socket.timeout:
            self.request.sendall(b"Request timed out waiting for delimiter.")
            return
        except Exception as e:
            self.request.sendall(b"Server error occurred")
            return




def readdata(filename="data.txt"):
    try: 
        with open(filename, "r") as file:
            lines = file.readlines()
            print("Loaded data.txt successfully.\n")
            return lines
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []


def parse_db(lines):
    db = []
    phonenumber = re.compile(r"^(394|426|901|514)-\d{4}$")
    for i in range(len(lines)):
        try:
            parts = lines[i].strip().split("|")
            if(len(parts) != 4):
                raise ValueError(f"DB read error. Record skipped [invalid formate]: {lines[i]}")
            if not parts[0]:
                raise ValueError(f"DB read error. Record skipped [null key field]: {lines[i]}")
            if parts[1]:
                if not parts[1].isdigit():
                    raise ValueError(f"DB read error. Record skipped [invalid age formate]: {lines[i]}")
                if(int(parts[1]) < 1 or int(parts[1]) > 120):
                    raise ValueError(f"DB read error. Record skipped [invalid age field]: {lines[i]}")
            if parts[3] and not phonenumber.match(parts[3]):
                    raise ValueError(f"DB read error. Record skipped [invalid phone field]: {lines[i]}")
            if any(data["name"].lower() == parts[0].lower() for data in db):
                raise ValueError(f"DB read error. Record skipped [key/record already exists]: {lines[i]}")
            db.append({
                "name": parts[0],
                "age" : parts[1],
                "address": parts[2],
                "phone#" : parts[3]
            })
        except ValueError as e:
            print(e)        
    return db


def write_file(filename="data_out.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for r in db:
            f.write(f"{r['name']}|{r['age']}|{r['address']}|{r['phone#']}\n")



if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    lines = readdata("data.txt")
    db = parse_db(lines)
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), server) as srv:
        print(f"\nServer is running... listening on {HOST}:{PORT}")
        srv.serve_forever()