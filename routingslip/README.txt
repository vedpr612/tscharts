Routing slip service

Routing slip is a list of station IDs associated with a clinic and patient.

routingslip
   get 
/tscharts/v1/routingslip/
   {patient:id, clinic:id}
   returns routing slip for patient, clinic pair
/tscharts/v1/routingslip/
   {clinic_id:id}
   returns array of routing slips ids corresponding to the specified clinic
/tscharts/v1/routingslip/id/
   returns routing slip with given ID 

   A routing slip looks like the following:

   { 
     -- routing slip id
     id: id,
     -- patient id
     patient: id,
     -- clinic ids
     clinic: id,
     -- how patient was categorized at registration (or later)
     -- will be reported as English text
     category: category,   
     -- array of routing slip entry ids in visitation order
     routing: routing, 
      -- array of commentids in timestamp order
      comments: comments,
    }
   post
/tscharts/v1/routingslip/
   {
    patient: id, -- required
    clinic: id,  -- required
    category: string,  -- required 
        valid values: "Dental", "Ortho", "New Cleft", "Returning Cleft",
        "Unknown", "Other" 
   }
   returns routing slip id 
   put
/tscharts/v1/routingslip/id/
   {category: category}    -- change category of patient}
   delete
/tscharts/v1/routingslip/id/

routingslipentry
    get
/tscharts/v1/routingslipentry/
    {routingslip:id, clinicstation:id}
    returns an ordered array of routingslip entries associated with a routing 
    slip and or a clinicstation
/tscharts/v1/routingslipentry/id/
    returns content of a routing slip entry for the given ID
    post
/tscharts/v1/routingslipentry/
    {routingslip:id, clinicstation:id}
    creates a routingslip entry. Initial state is scheduled. Initial order
    relative to other entries is undefined. Use put to set order and/or to
    change state
    put
/tscharts/v1/routingslipentry/id/
    {order:order, state:state}
    valid states "Scheduled", "Checked In", "Checked Out", "Removed"
    one or both of the above params are updated
    delete
/tscharts/v1/routingslipentry/id/

routingslipcomment
    get
/tscharts/v1/routingslipcomment/
    {routingslip:id}
    returns an ordered (by timestamp) array of routingslip comment IDs 
/tscharts/v1/routingslipcomment/id/
    returns a routing slip comment for the given record ID
    format of data:
    {id: id, comment:comment, author:id, timestamp:timestamp}
    post
/tscharts/v1/routingslipcomment/
    {routingslip:id, comment:text, author:id}
    creates a routingslip comment.
    delete
/tscharts/v1/routingslipcomment/id/

