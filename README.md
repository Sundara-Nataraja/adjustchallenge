# adjustchallenge

Framework used : django & django-rest-framework 

The AD campaign Url can be accessed using **<ip>/campaigns/cpi/ <br/>**
API could be version also but for assignment ihave not opted it
  
  1) Filtering can be applied on **Columnname** via date(=,__gte,__lte,__gt,__lt) , country(=),channel(=),os(=)
      eg: date__lte=2017-06-01
  2) Grouping/Breakdown can be applied by using queryparam -> **groupby**
      eg:groupby=channel,country
  3) Ordering can be applied any column : **columnname** --> ascending / **-columnname** --> decending
      eg:ordering=-channel,country
      
  4) desired Column can be dynamically get using **columns** query params
      eg: columns=impressions,clicks
  5) To get CPI please inculde cpi in columns queryparam:
      eg: column=installs,cpi
  
Usecases with urls:
  
  1) Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
  ```  
  /campaigns/cpi/?date__lte=2017-06-01&groupby=channel,country&columns=impressions,clicks&ordering=-clicks
  ```

2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
  ```
  /campaigns/cpi/?date__gte=2017-05-01&date__lte=2017-05-31&os=ios&groupby=date&columns=installs&ordering=-date
  ```
3) Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
  ```
  /campaigns/cpi/?date=2017-06-01&country=US&groupby=os&columns=revenue&ordering=-revenue
  ```
4) Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.
 ```
  /campaigns/cpi/?country=CA&groupby=channel&columns=cpi,spend&ordering=-cpi
  ```
  
  
  
  
  
  
  
