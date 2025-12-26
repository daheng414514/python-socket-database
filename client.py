import socket

HOST, PORT = "localhost", 9999

def send_message(msg: str) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((HOST, PORT))
            sock.sendall((msg + "\n").encode("utf-8"))
            total_message = []
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                total_message.append(data)
            reply = b"".join(total_message).decode("utf-8")
            return reply
    except Exception as e:
        print("Debug: ", e)
        return "Connection error. Please try again...\n"


def has_pipe(*fields):
    return any("|" in (field or "") for field in fields)

def isempty(*fields):
    return any((not field.strip()) for field in fields)

if __name__ == "__main__":
    while True:
        print("\nPython Database Menu\n")
        print("1. Find Customer")
        print("2. Add Customer")
        print("3. Delete Customer")
        print("4. Update Customer Age")
        print("5. Update Customer Address")
        print("6. Update Customer Phone")
        print("7. Print Report")
        print("8. Update File and Exit\n")
        first_msg = input("\nSelect: ").strip()
        
        if first_msg == "1":
            second_msg = input("\nCustomer name: ").strip()
            if has_pipe(second_msg):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(second_msg):
                print("\nName cannot be empty.") 
                continue
            msg = first_msg + "|" + second_msg



        elif first_msg == "2":
            name = input("\nCustomer name: ").strip()
            age = input("\nCustomer age: ").strip()
            address = input("\nCustomer address: ").strip()
            phone = input("\nCustomer phone: ").strip()
            if has_pipe(name, age, address, phone):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(name, age):
                print("\nName and age cannot be empty.") 
                continue
            msg = first_msg + "|" + name + "|" + age + "|" + address + "|" + phone



        elif first_msg == "3":
            second_msg = input("\nCustomer name: ").strip()
            if has_pipe(second_msg):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(second_msg):
                print("\nName cannot be empty.") 
                continue
            msg = first_msg + "|" + second_msg



        elif first_msg == "4":
            name = input("\nCustomer name: ").strip()
            age = input("\nCustomer age: ").strip()
            if has_pipe(name, age):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(name, age):
                print("\nName and age cannot be empty.") 
                continue
            msg = first_msg + "|" + name + "|" + age



        elif first_msg == "5":
            name = input("\nCustomer name: ").strip()
            address = input("\nCustomer address: ").strip()
            if has_pipe(name, address):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(name):
                print("\nName cannot be empty.") 
                continue
            msg = first_msg + "|" + name + "|" + address



        elif first_msg == "6":
            name = input("\nCustomer name: ").strip()
            phone = input("\nCustomer phone: ").strip()
            if has_pipe(name, phone):
                print("\n'|' is not accepted as input. Please try again.") 
                continue
            if isempty(name):
                print("\nName cannot be empty.") 
                continue
            msg = first_msg + "|" + name + "|" + phone



        elif first_msg == "7":
            msg = first_msg



        elif(first_msg == "8"):
            msg = first_msg
            print("\nStart shutting down the server...\n")
            
        
        else:
            print("\nInvalid choice...") 
            continuekey = input("\n\nPress any key to continue...")
            continue

        resp = send_message(msg)
        print("\nServer replied:", resp)
        

        if first_msg == "8":
            print("\nGood bye~\n")
            break

        continuekey = input("\n\nPress any key to continue...")