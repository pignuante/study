[TOC]



## SQL은 무엇인가?

1. SQL은 구조적 *query*언어를 의미.
2. *Database*를 조작하는데 사용한다.
3. *ANSI*표준이다.



## SQL은 무엇을 할 수 있을까?

1. DataBase에 *query*를 실행할 수 있다.
2. DataBase에서 데이터를 검색 할 수 있다.
3. DataBase에 자료를 **insert**, **update**, **delete**할 수 있다.
4. 새 DataBase를 만들 수 있다.



## SQL 구문

|       이름        |       설명       |
| :-------------: | :------------: |
|     SELECT      |  DB에서 데이터를 추출  |
|     UPDATE      | DB에서 데이터를 업데이트 |
|     DELETE      |  DB에서 데이터를 삭제  |
|   INSERT INTO   | DB에 새 데이터를 삽입  |
| CREATE DATABASE |    새 DB를 생성    |
| ALTER DATABASE  |     DB를 수정     |
|  CREATE TABLE   |  새로운 table 생성  |
|   ALTER TABLE   |    table 수정    |
|   DROP TABLE    |    table 삭제    |
|  CREATE INDEX   |   index를 생성    |
|   DROP INDEX    |   index를 삭제    |



#### SQL SELECT 문

```sql
SELECT * FROM Customer;
SELECT Name, City FROM Customer;
```

- **SELECT**문은 데이터 베이스에서 데이터를 선택하는데 사용된다.
- `SELECT coloumn1, ..., columnN FROM tableName`의 형태로 사용된다.



#### SQL SELECT DISTINCT 문

```sql
SELECT DISTINCT Country FROM Customers;

/*for MS DB*/
SELECT Count(*) AS DistinctCountries
FROM (SELECT DISTINCT Country FROM Customers);
```

- **SELECT DISTINCT**문은 column의 결과값에 중복된 값을 제거해 준다.
- `SELECT DISTINCT column1, ..., columnN FROM tableName`의 형태로 사용된다.



#### SQL WHERE 문

```sql
SELECT * FROM Customers
WHERE Country="Mexico";

SELECT name FROM Customers
WHERE CustomerID=1;
```

- **WHERE**문은 주로 자료에 대해 *filter*의 기능을 수행할때 사용된다.
- `SELECT coloumn1, ..., columnN FROM tableName WHERE condition;`의 형태로 쓰인다.

| 연산자     | 설명                                       |
| :------ | :--------------------------------------- |
| =       | Equal                                    |
| <>, !=  | Not Equal                                |
| >       | Greater than                             |
| <       | Less than                                |
| \>=     | Greater than equal                       |
| <=      | Less than or equal                       |
| BETWEEN | Between an inclusive range               |
| LIKE    | Search for pattern                       |
| IN      | To specify multiple possible values for a column |

#### SQL AND, OR and NOT operator

```sql
SELECT * FROM Customers
WHERE Country="Germany" AND City="Berilin";

SELECT * FROM Customers
WHERE City="Seoul" OR City="Busan";

SELECT * FROM Customers
WHERE NOT City="MokPo";

SELECT * FROM Customers
WHERE Country="Korea" AND (City="Seoul" OR City="Daegu")
```



#### SQL ORDER BY keyword

1. ORDER BY 예시

   ```sql
   SELECT * FROM Customers
   ORDER BY Country;
   ```

   Customers에서 Country의 오름차순으로 정렬한다.

2. ORDER BY DESC 예시

   ```sql
   SELECT * FROM Customers
   ORDER BY Country DESC;
   ```

   Customers에서 Country의 내림차순으로 정렬한다.

3. 다수의 Column 예시

   ```sql
   /*1*/
   SELECT * FROM Customers
   ORDER BY Country, CustomerName;

   /*2*/
   SELECT * FROM Customers
   ORDER BY CustomerName, Country;

   SELECT * FROM Customers
   ORDER BY Country ASC, CustomerName DESC;
   ```

   - 첫번째의 경우 Customers에서 Country로 정렬을 한 후, 그 안에서 CustomerName으로 다시 정렬을 한다.
   - 두번째의 경우 Customers에서 CustomerName으로 정렬을 한 후, 그 안에서 Country로 다시 정렬한다.



#### SQL INSERT INTO 문

1. INSERT INTO 예문

   ```sql
   INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
   VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
   ```

   Customers의 모든 column에 자료를 넣은 예시이다. 만약 모든 column에 자료를 넣을때는 column명을 생략가능하다.



#### SQL *NULL* value

```sql
SELECT LastName, FirstName, Address FROM Persons
WHERE Address IS NULL;

SELECT LastName, FirstName, Address FROM Persons
WHERE Address IS NOT NULL;
```

> NULL value는 데이터 필드에서 아무런 값이 없는 것을 의미한다. (0의 값이 들어있는것이랑은 다르다.)
>
> 데이터 필드에 NULL의 존재 여부는 DB를 생성할때 미리 정해진다.
>
> NULL은 일반 comparison operator로는 비교가 불가하며, **IS NULL** 혹은 **IS NOT NULL**로만 비교가 가능하다.



#### SQL UPDATE 문

```sql
UPDATE Customers
SET ContactName = 'Alfred Schmidt', City= 'Frankfurt'
WHERE CustomerID = 1;

UPDATE Customers
SET ContactName='Juan'
WHERE Country='Mexico';
```

UPDATE문은 이미 table에 존재하는 자료의 값을 수정할때 사용된다.



#### SQL DELETE 문

```sql
DELETE FROM Customers
WHERE CustomerName='Alfreds Futterkiste';

DELETE * FROM table_name;
```

DELETE문은 테이블에 존재하는 자료를 지울때 사용된다.



#### SQL IN 연산자

```sql
SELECT * FROM Customers
WHERE Country IN ('Germany', 'France', 'UK');

SELECT * FROM Customers
WHERE Country NOT IN ('Germany', 'France', 'UK');

SELECT * FROM Customers
WHERE Country IN (SELECT Country FROM Suppliers);
```

IN 연산자는 WHERE문에서의 결과값을 특정화 시켜줄때 사용된다. IN연산자를 사용함으로 다중 OR문을 짧게 줄일수 있다.



#### SQL BETWEEN 연산자

```sql
SELECT * FROM Products
WHERE Price BETWEEN 10 AND 20;

SELECT * FROM Products
WHERE Price NOT BETWEEN 10 AND 20;

SELECT * FROM Products
WHERE (Price BETWEEN 10 AND 20)
AND NOT CategoryID IN (1,2,3);

SELECT * FROM Products
WHERE ProductName NOT BETWEEN 'Carnarvon Tigers' AND 'Mozzarella di Giovanni'
ORDER BY ProductName;

SELECT * FROM Orders
WHERE OrderDate BETWEEN #07/04/1996# AND #07/09/1996#;
```

BETWEEN연산자는 주어진 범위내에서 결과값을 찾는 연산자이다.



#### SQL Joins

Join문은 다수의 table의 row를 합칠때 사용된다.

|         이름         |             설명              |
| :----------------: | :-------------------------: |
|    (INNER)Join     |       양 테이블에 매치가 되는 값       |
| LEFT (OUTER) Join  |  left의 모든 값 + 매칭되는 right값   |
| RIGHT (OUTER) Join |  right의 모든 값 + 매칭되는 left값   |
| FULL (OUTER) Join  | left나 right에 하나라도 매치되는 모든 값 |



###### SQL Inner Join

![Inner Join](https://www.w3schools.com/sql/img_innerjoin.gif)

```sql
SELECT Orders.OrderID, Customers.CustomerName
FROM Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;

SELECT Orders.OrderID, Customers.CustomerName, Shippers.ShipperName
FROM ((Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID)
INNER JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID);
```

INNER JOIN은 양 table에 둘다 정의되어 있는 자료를 선택한다.



###### SQL LEFT, RIGHT (OUTER) JOIN

![LEFT JOIN](https://www.w3schools.com/sql/img_leftjoin.gif)



```sql
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
ORDER BY Customers.CustomerName;
```

LEFT JOIN은 LEFT TABLE의 모든 값을 출력하고, RIGHT TABLE의 결과값이 매치되는 값만 출력한다. 만약 매치되지 않으면 NULL을 출력한다.



![RIGHT JOIN](https://www.w3schools.com/sql/img_rightjoin.gif)

```sql
SELECT Orders.OrderID, Employees.LastName, Employees.FirstName
FROM Orders
RIGHT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
ORDER BY Orders.OrderID;
```

RIGHT JOIN은 LEFT와 반대이다.



###### SQL FULL (OUTER) JOIN

![](https://www.w3schools.com/sql/img_fulljoin.gif)



```sql
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
FULL OUTER JOIN Orders ON Customers.CustomerID=Orders.CustomerID
ORDER BY Customers.CustomerName;
```

FULL JOIN은 LEFT와 RIGHT JOIN을 합친 것이다. 각각에 포함되지 않은 것들의 NULL값까지 다 표현이 된다.



###### SQL SELF JOIN

```sql
SELECT A.CustomerName AS CustomerName1, B.CustomerName AS CustomerName2, A.City
FROM Customers A, Customers B
WHERE A.CustomerID <> B.CustomerID
AND A.City = B.City 
ORDER BY A.City;
```

SELF JOIN은 자기 자신을 JOIN하는 것이다.

> 이름이 SMITH인 사원의 매니저 이름을 알아내려면 이 역시 EMP테이블에서 확인 할 수 있다. 그럼 담당 매니저의 이름을 알아내려면 어떻게 해야할까? 매니저 테이블이 있다면 이 두 테이블을 조인하여 알아낼 수 있겠지만 매니저 역시 이 회사에 사원이기 때문에 중복된 데이터가 생길 수 있으므로 SMITH 담당 매니저의 정보는 사원 테이블을 참조해서 얻어내야 한다. 이렇게 **자신과 자기 자신을 조인하는것이 SELF JOIN이라고 한다.**



#### UNION 연산자

```sql
SELECT City FROM Customers
UNION
SELECT City FROM Suppliers
ORDER BY City;

SELECT City, Country FROM Customers
WHERE Country='Germany'
UNION
SELECT City, Country FROM Suppliers
WHERE Country='Germany'
ORDER BY City;

SELECT City, Country FROM Customers
WHERE Country='Germany'
UNION ALL
SELECT City, Country FROM Suppliers
WHERE Country='Germany'
ORDER BY City;

SELECT 'Customer' As Type, ContactName, City, Country
FROM Customers
UNION
SELECT 'Supplier', ContactName, City, Country
FROM Suppliers;
```

UNION operator는 여러개의 SELECT문의 결과를 합칠때 사용되어진다.



#### SQL GROUP BY 문

```sql
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country;

SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country
ORDER BY COUNT(CustomerID) DESC;

SELECT Shippers.ShipperName, COUNT(Orders.OrderID) AS NumberOfOrders FROM Orders
LEFT JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID
GROUP BY ShipperName;
```

GROUP BY 문은 결과로 나온 값들을 *COUNT*, *MAX*, *MIN*, *SUM*, *AVG*로 다시한번 묶어주는 역할을 한다.



#### SQL EXISTS operator

```sql
SELECT SupplierName
FROM Suppliers
WHERE EXISTS (SELECT ProductName FROM Products WHERE SupplierId = Suppliers.supplierId AND Price < 20);

SELECT SupplierName
FROM Suppliers
WHERE EXISTS (SELECT ProductName FROM Products WHERE SupplierId = Suppliers.supplierId AND Price = 22);
```

EXISTS 연산자는 데이터의 존재여부를 확인할떄 쓰인다. 결과에 맞는 값이 존재할때 true를 리턴한다.





#### SQL ANY and ALL operator

```sql
/*ANY*/
SELECT ProductName
FROM Products
WHERE ProductID = ANY (SELECT ProductID FROM OrderDetails WHERE Quantity = 10);

SELECT ProductName
FROM Products
WHERE ProductID = ANY (SELECT ProductID FROM OrderDetails WHERE Quantity > 99);
```

ANY 연산자는 조건을 만족하는 것이 하나라도 존재 할시 true를 리턴한다.



```sql
/*ALL*/
SELECT ProductName
FROM Products
WHERE ProductID = ALL (SELECT ProductID FROM OrderDetails WHERE Quantity = 10);
```

ALL 연산자는 모든 것이 조건을 만족 할 시 true를 리턴한다.































