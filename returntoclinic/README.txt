Return to clinic service

returntoclinic
   get 
/tscharts/v1/returntoclinic/id/
   returns returntoclinic with given ID
   {patient:id, clinic:id, station:id, interval:number_of_months, month:integer, year:integer}
   In above, month is in range [1-12], year is 4 digit e.g., 2017
/tscharts/v1/returntoclinic/
   {patient:id, clinic:id, station:id}
   above parameters filter if present
   if station is specified, either patient or clinic should be specified
   to be meaningful, but this is not enforced
   returns array of matching return to clinic ids
   post
/tscharts/v1/returntoclinic/
   {patient:id, clinic:id, station:id, interval:number_of_months}
   returns returntoclinic id 
   put
/tscharts/v1/returntoclinic/id/
   {interval:number_of_months}
   delete
/tscharts/v1/returntoclinic/id/

