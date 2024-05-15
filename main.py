from dao import Carmanagement,CustomerRepository,PaymentHandler,LeaseRepository

class Main:
    def carmanagement():
        print("1.add car")
        print("2.remove car")
        print("3.List available cars")
        print("4.List rented cars")
        print("5.find car by id")
        print("6. exit")
    
    def customermanagement():
        print("1. Add a new customer")
        print("2. Remove a customer")
        print("3. List all customers")
        print("4. Find customer by ID")
        print("5. exit")
    def LeaseManagement():
        print("1. Create a new lease")
        print("2. Return a leased car")
        print("3. List all active leases")
        print("4. List lease history")
        print("5. exit")
    def paymentHandling():
        print("1. Record a payment")
        print("2.Exit")
    def mainmenu():
        print("1. Car Management")
        print("2. Customer Management")
        print("3. Lease Management")
        print("4. payment Management")
        print("5. Break")


    while True:
        mainmenu()
        mm_choice=int(input("Enter your choice: "))
        if mm_choice==1:
            carobj=Carmanagement()
            while True:
                carmanagement()
                choice=int(input("Enter your choice: "))
                if choice==1:
                    vehicle_id = input("Enter vehicle ID: ")
                    make = input("Enter make: ")
                    model = input("Enter model: ")
                    year = input("Enter year: ")
                    daily_rate = input("Enter daily rate: ")
                    status = input("Enter status: ")
                    passenger_capacity = input("Enter passenger capacity: ")
                    engine_capacity = input("Enter engine capacity: ")

                    car = {
                        "vehicleID": vehicle_id,
                        "make": make,
                        "model": model,
                        "year": year,
                        "dailyRate": daily_rate,
                        "status": status,
                        "passengerCapacity": passenger_capacity,
                        "engineCapacity": engine_capacity
                    }
                    
                    carobj.addCar(car)
                elif choice==2:
                    carid=int(input("Enter the carId you wanna remove: "))
                    carobj.removeCar(carid)
                elif choice==3:
                    carobj.listAvailableCars()
                elif choice==4:
                    carobj.listRentedCars()
                elif choice==5:
                    id=int(input("Enter the carId: "))
                    carobj.findCarById(id)
                elif choice==6:
                    carobj.close()
                    break
                else:
                    print("Please enter numbers within range")
        elif mm_choice==2:
            customerobj=CustomerRepository()
            while True:
                customermanagement()
                choice=int(input("Enter your choice: "))
                if choice==1:
                    customer_id = input("Enter Customer ID: ")
                    first_name = input("Enter First Name: ")
                    last_name = input("Enter Last Name: ")
                    email = input("Enter Email: ")
                    phone_number = input("Enter Phone Number: ")
                    new_customer = {
                        "CustomerID": customer_id,
                        "firstName": first_name,
                        "lastName": last_name,
                        "email": email,
                        "phoneNumber": phone_number
                    }

                    customerobj.addCustomer(new_customer)
                elif choice==2:
                    id=int(input("Enter the customer id you wanna remove: "))
                    customerobj.removeCustomer(id)
                elif choice==3:
                    customerobj.listCustomers()
                elif choice==4:
                    id=int(input("Enter the id of the customer you want to find: "))
                    customerobj.findCustomerById(id)
                elif choice==5:
                    customerobj.close()
                    break
                else:
                    print("Please enter numbers within range") 
        elif mm_choice==3:
            leaseobj=LeaseRepository()
            while True:
                LeaseManagement()
                choice=int(input("Enter your choice: "))
                if choice==1:
                    customer_id = input("Enter Customer ID: ")
                    vehicle_id = input("Enter Vehicle ID: ")
                    start_date = input("Enter Start Date (YYYY-MM-DD): ")
                    end_date = input("Enter End Date (YYYY-MM-DD): ")
                    lease_type = input("Enter Lease Type: DailyLease/MonthlyLease")
                    leaseobj.createLease(customer_id,vehicle_id,start_date,end_date,lease_type)
                elif choice==2:
                    id=int(input("Enter the ID of the lease: "))
                    leaseobj.returnCar(id)
                elif choice==3:
                    leaseobj.listActiveLeases()
                elif choice==4:
                    leaseobj.listLeaseHistory()
                elif choice==5:
                    leaseobj.close()
                    break
                else:
                    print("Please enter numbers within range") 
        elif mm_choice==4:
            paymentobj=PaymentHandler()
            while True:
                paymentHandling()
                choice=int(input("Enter your choice: "))
                if choice==1:
                    leaseid=int(input("Enter the leaseID the payment belongs too: "))
                    amount=int(input("Enter the payment amount: "))
                    paymentobj.recordPayment(leaseid,amount)
                elif choice==2:
                    paymentobj.close()
                    break
                else:
                    print("Please enter numbers within range") 
        elif mm_choice==5:
            print("Thanks for using our application :D")
            break
        else:
            print("Please enter numbers within range") 

obj=Main()