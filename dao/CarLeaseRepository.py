from .ICarLeaseRepository import*
from .Entity import Customer,Vehicle
from .util import Db_prop,DBConnutil
from tabulate import tabulate
from .exception import AddCarException,UpdateCarException,AddCustomerException,CreateLeaseException,RetrieveCarException,CarManagementException,RecordPaymentException,UpdateCustomerException,LeaseManagementException,PaymentHandlingException,CalculateRevenueException,RetrieveCustomerException,CalculateLeaseCostException,RetrievePaymentHistoryException

class Carmanagement(ICarManagementRepository):
    def __init__(self) -> None:
        self.connection=DBConnutil.get_connectionOBJ(Db_prop.getconstring())
        self.cursor=self.connection.cursor()
    def addCar(self, car):
        new_vehicle=Vehicle(car["vehicleID"], car["make"], car["model"], car["year"], car
                            ["dailyRate"], car["status"], car["passengerCapacity"], car["engineCapacity"])
        try:
            self.cursor.execute("INSERT INTO Vehicle (vehicleID, make, model, year, dailyRate, status, passengerCapacity, engineCapacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (new_vehicle.getVehicleID(), new_vehicle.getMake(), new_vehicle.getModel(), new_vehicle.getYear(), new_vehicle.getDailyRate(), new_vehicle.getStatus(), new_vehicle.getPassengerCapacity(), new_vehicle.getEngineCapacity()))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise UpdateCarException(f"Cant update")
    def removeCar(self, carID):
        try:
            self.cursor.execute("DELETE FROM Vehicle WHERE vehicleID=?", (carID,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise UpdateCarException(f"Cant find car with id {carID}")
    def listAvailableCars(self):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE status = 'available'")
            available_cars = self.cursor.fetchall()
            print(tabulate(available_cars))
        except Exception as e:
            self.connection.rollback()
            raise RetrieveCarException("couldn't retrive")   

    def listRentedCars(self):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE status = 'notAvailable'")
            available_cars = self.cursor.fetchall()
            print(tabulate(available_cars)) #list of tuples
        except Exception as e:
            self.connection.rollback()
            raise RetrieveCarException("couldn't retrive")   
    def findCarById(self, carID):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = ?",(carID))
            available_cars = self.cursor.fetchone()
            print(available_cars)#list of tuple
        except Exception as e:
            self.connection.rollback()
            raise RetrieveCarException(f"Cant find a car with id {carID}")
    def close(self):
        self.cursor.close()
        self.connection.close() 

class CustomerRepository(ICustomerRepository):
    def __init__(self) -> None:
        self.connection=DBConnutil.get_connectionOBJ(Db_prop.getconstring())
        self.cursor=self.connection.cursor()
    def addCustomer(self,customer):
        new_customer=Customer(customer["CustomerID"],customer["firstName "],customer["lastName"],
                              customer["email"],customer["phoneNumber"])
        try:
            self.cursor.execute("Insert into Customer (customerId,firstName,lastName,email,phoneNumber) Values (?,?,?,?,?)",
                                (new_customer.getCustomerID(),new_customer.getFirstName(),new_customer.getLastName(),new_customer.getEmail(),new_customer.getPhoneNumber()))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise AddCarException("Could'nt add")   
    def removeCustomer(self, customerID):
        try:
            self.cursor.execute("DELETE FROM Customer WHERE customerID = ?", (customerID,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise RetrieveCustomerException(f"Customer with id {customerID} does not exists") 
    def listCustomers(self):
        try:
            self.cursor.execute("SELECT * FROM Customer")
            print(tabulate(self.cursor.fetchall()))
        except Exception as e:
            raise RetrieveCustomerException("customer table is empty")
    def findCustomerById(self, customerID):
        try:
            self.cursor.execute("SELECT * FROM Customer WHERE customerID = ?", (customerID,))
            print(self.cursor.fetchone())
        except Exception as e:
            raise RetrieveCustomerException(f"There is no customer with id {customerID}") 
    def close(self):
        self.cursor.close()
        self.connection.close() 

class LeaseRepository(ILeaseRepository):
    def __init__(self) -> None:
        self.connection=DBConnutil.get_connectionOBJ(Db_prop.getconstring())
        self.cursor=self.connection.cursor()

    def createLease(self, customerID, carID, startDate, endDate,leaseType):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO Lease (customerID, vehicleID, startDate, endDate, leaseType) VALUES (?, ?, ?, ?, ?)",
                               (customerID, carID, startDate, endDate, leaseType))
            self.connection.commit()
        except Exception as e:
            raise LeaseManagementException("Coudlnt add lease")
    def returnCar(self, leaseID):
        try:
            self.cursor.execute("SELECT * FROM Lease WHERE leaseID = ?", (leaseID,))
            print(tabulate(self.cursor.fetchall()))
        except Exception as e:
            raise RetrieveCarException(f"cant find car with leaseId{leaseID}") 
    def listActiveLeases(self):
        try:
            self.cursor.execute("SELECT * FROM Lease WHERE endDate>=GETDATE()")
            print(tabulate(self.cursor.fetchall()))
        except Exception as e:
            raise LeaseManagementException("There is no active leases")
    def listLeaseHistory(self):
        try:
            self.cursor.execute("SELECT * FROM Lease")
            print(tabulate(self.cursor.fetchall()))
        except Exception as e:
            raise LeaseManagementException("Lease table is empty")
    def close(self):
        self.cursor.close()
        self.connection.close() 

class PaymentHandler(IPaymentHandler):
    def __init__(self) -> None:
        self.connection=DBConnutil.get_connectionOBJ(Db_prop.getconstring())
        self.cursor=self.connection.cursor() 
    def recordPayment(self, leaseID, amount):
        try:
            self.cursor.execute("SELECT paymentID FROM Payment ORDER BY paymentID DESC offset 0 rows fetch next 1 rows only;")
            currentpaymentId=self.cursor.fetchone()
            self.cursor.execute("Insert into payment (paymentId,leaseId,paymentDate,amount) Values (?,?,GETDATE(),?)",(currentpaymentId[0]+1,leaseID,amount))
        except Exception as e:
            raise RecordPaymentException(f"Invalid leaseId")
    def close(self):
        self.cursor.close()
        self.connection.close() 
