from ICarLeaseRepository import*
from Vehicle import Vehicle
from Customer import Customer
from db_prop import Db_prop
from DBConnutil import DBConnutil
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
            raise e
    def removeCar(self, carID):
        try:
            self.cursor.execute("DELETE FROM Vehicle WHERE vehicleID=?", (carID,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
    def listAvailableCars(self):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE status = 'available'")
            available_cars = self.cursor.fetchall()
            return available_cars #list of tuples
        except Exception as e:
            self.connection.rollback()
            raise e   

    def listRentedCars(self):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE status = 'notAvailable'")
            available_cars = self.cursor.fetchall()
            return available_cars #list of tuples
        except Exception as e:
            self.connection.rollback()
            raise e   

    def findCarById(self, carID):
        try:
            self.cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = ?",(carID))
            available_cars = self.cursor.fetchone()
            return available_cars #list of tuple
        except Exception as e:
            self.connection.rollback()
            raise e
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
            raise e   
    def removeCustomer(self, customerID):
        try:
            self.cursor.execute("DELETE FROM Customers WHERE customerID = ?", (customerID,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e  
    def listCustomers(self):
        try:
            self.cursor.execute("SELECT * FROM Customers")
            return self.cursor.fetchall()
        except Exception as e:
            raise e
    def findCustomerById(self, customerID):
        try:
            self.cursor.execute("SELECT * FROM Customers WHERE customerID = ?", (customerID,))
            return self.cursor.fetchone()
        except Exception as e:
            raise e 
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
            raise e
    def returnCar(self, leaseID):
        try:
            self.cursor.execute("SELECT * FROM Lease WHERE leaseID = ?", (leaseID,))
            return self.cursor.fetchall()
        except Exception as e:
            raise e 
    def listActiveLeases(self):
        try:
            self.cursor.execute("SELECT * FROM Lease WHERE endDate>=GETDATE()")
            return self.cursor.fetchall()
        except Exception as e:
            raise e
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
            raise e
    def close(self):
        self.cursor.close()
        self.connection.close() 