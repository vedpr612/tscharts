**Get Surgery History**
----
  Returns json data about a single surgeryhistory resource. 

* **URL**

  /tscharts/v1/surgeryhistory/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"patientid":id,"patientname": string,"surgeryname": string,"surgeryyear":integer,"surgerymonth":integer,"surgerylocation": string, "anesthesia_problems":[true|false], "bleeding_problems":[true|false]}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST
  * **Code:** 404 NOT FOUND
  * **Code:** 500 INTERNAL ERROR

* **Example:**

```
GET /tscharts/v1/surgeryhistory/1/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


{"patientid":1,"surgeryname":surgery1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}
```
  
**Get Multiple Surgery Histories**
----
  Returns data about all matching surgeryhistory resources.

* **URL**

  /tscharts/v1/surgeryhistory/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `patient` patient id<br />

   **Optional:**
 
   `surgeryname` string<br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"patientid":id,"patientname": string,"surgeryname": string,"surgeryyear":integer,"surgerymonth":integer,"surgerylocation": string, "anesthesia_problems":[true|false], "bleeding_problems":[true|false]},...]`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/surgeryhistory/?patientid=5 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Sat, 29 Jul 2017 22:36:22 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


[{"patientid":5,"surgeryname":surgery1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}, {"patientid":5,"surgeryname":surgery2,"surgeryyear":2005,"surgerymonth":5,"surgerylocation":place2,"anesthesia_problems":false,"bleeding_problems":true}]
```
  
**Create Surgery History**
----
  Create a surgeryhistory instance.

* **URL**

  /tscharts/v1/surgeryhistory/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
   `patientid` patient id<br />
   `surgeryname` string the surgery name<br />
   `surgeryyear` integer legal year<br />
   `surgerymonth` integer legal month<br />
   `surgerylocation` string the location where the surgery performed<br />
   `anesthesia_problems` [true|false] whether the patient has problems with the anesthesia<br />
   `bleeding_problems` [true|false] whether the patient has bleeding problems<br />

   **Optional:**
 
   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":id}`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/surgeryhistory/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 48
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"patientid":5,"surgeryname":surgery1,"surgeryyear":1999,"surgerymonth":12,"surgerylocation":place1,"anesthesia_problems":true,"bleeding_problems":false}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:15 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{"id":12}
```

**Update Surgery History**
----
  Update a surgeryhistory instance.

* **URL**

  /tscharts/v1/surgeryhistory/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following is required. 
 
   `surgeryname` the surgery name string<br />
   `surgeryyear` legal year<br />
   `surgerymonth` legal month<br />
   `surgerylocation` the location where the surgery performed string<br />
   `anesthesia_problems` [true|false] whether the patient has problems with the anesthesia<br />
   `bleeding_problems` [true|false] whether the patient has bleeding problems<br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**
  
  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/clinicstation/30/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 33
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"surgeryyear": 2012, "surgerymonth":8}HTTP/1.0 200 OK
Date: Wed, 26 Apr 2017 05:29:17 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete Surgery History**
----
  Delete a surgeryhistory instance. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/surgeryhistory/id

* **Method:**

  `DELETE`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
DELETE /tscharts/v1/surgeryhistory/200/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Tue, 18 Apr 2017 20:17:14 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

