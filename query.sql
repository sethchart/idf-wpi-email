SELECT 
    cc.id AS Contact_ID,
    cc.first_name AS First_Name,
    cc.last_name AS Last_Name,
    cem.email AS Email,
    CASE
        WHEN gc.status LIKE 'Added' THEN 'True'
        ELSE NULL
    END AS Walk_Email_Subscribed,
    cev.title AS Event_Registered,
    ca.geo_code_2 AS Lon,
    ca.geo_code_1 AS Lat
FROM
    civicrm_contact AS cc
        LEFT OUTER JOIN
    civicrm_group_contact AS gc ON gc.contact_id = cc.id
        AND gc.group_id in (956, 957)
        AND gc.status LIKE 'Added'
        LEFT OUTER JOIN
    civicrm_participant AS cp ON cp.contact_id = cc.id
        AND cp.status_id = 1
        AND cp.event_id IN {0}
        LEFT OUTER JOIN
    civicrm_event AS cev ON cev.id = cp.event_id
        LEFT OUTER JOIN
    civicrm_address AS ca ON ca.contact_id = cc.id
        AND ca.is_primary = 1
        LEFT OUTER JOIN
    civicrm_state_province AS sp ON sp.id = ca.state_province_id
        JOIN
    civicrm_email AS cem ON cem.contact_id = cc.id
        AND cem.is_primary = 1
        AND cem.on_hold = 0
WHERE
    cc.contact_type LIKE 'Individual'
        AND cc.is_deceased = 0
        AND cc.is_deleted = 0
        AND cc.do_not_email = 0
        AND cc.is_opt_out = 0
        AND (gc.status LIKE 'Added'
        OR cev.id IS NOT NULL)
        group by cc.id
