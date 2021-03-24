---
title: "Docker Template: Python App Looped Execution"
date: 2021-03-24T16:00:00-23:30:00
categories:
  - walkthrough
tags:
  - walkthrough
  - python
  - docker
excerpt: "Generate custom datasets from randomized data into csv, xml, and parquet"
---

# Auto Generate Lab Measurement Dataset
---------------------------

A typical data source found in most industrial work places are lab measurements. This type of data usually has a well defined structure and is a mixture of categorical and numeric data types. Measurement ranges and file format can vary greatly between use cases. This article covers how to generate a simple dataset that can be customized to simulate a wide range of use cases.  

## Contents
1. Data Structure
2. Packages
    - Faker
    - xml.etree.ElementTree
    - Pandas
3. Generate Dataset
4. Convert Dataset to XML
5. Convert Dataset to Pandas DataFrame
6. Save File
    - csv
    - xml
    - parquet

## Sample Data Structure

| Field          | DataType    | Min  | Max  |
|----------------|-------------|------|------|
| machine_id     | string      |      |      |
| test_id        | uuid        |      |      |
| technician     | string      |      |      |
| test_routine   | categorical |      |      |
| batched        | categorical |      |      |
| loc_1          | dictionary  |      |      |
| loc_1_x_offset | decimal     | -15  | 15   |
| loc_1_y_offset | decimal     | -1   | 1    |
| loc_1_z_offset | int         | 2500 | 5000 |
| loc_2          | dictionary  |      |      |
| loc_2_x_offset | decimal     | -15  | 15   |
| loc_2_y_offset | decimal     | -1   | 1    |
| loc_2_z_offset | int         | 2500 | 5000 |

## Packages

**Faker:** Is a python package for creating, as the name implies, fake data. This library not only generates random numbers and strings but more complex elements like addresses, and names.


```python
from faker import Faker
fake = Faker()
Faker.seed(0)
```

**xml.etree.ElementTree:** Is a base library of Python that is a simple and efficient way of querying, parsing, and creating XML data.


```python
import xml.etree.ElementTree as ET
from xml.dom import minidom
```

**Pandas:** Is the goto library for working with table-like data.


```python
import pandas as pd
```


```python
# base imports
import uuid
import os
```

## Generate Dataset

The structure of the dataset is represented  by a dictionary and uses Faker to fill in the data values. This allows for simple modifications when moving between use cases.   


```python
def generate_measurement_record():
    base_equipment_name='Machine'
    equipment_cnt = 25
    n = fake.pyint(min_value=1, max_value=equipment_cnt)

    measurement_record = {
        'machine_id': '_'.join([base_equipment_name, f'{n:02}'])
        ,'test_id':str(uuid.uuid4().hex)
        ,'technician':fake.name()
        ,'test_routine':fake.random_sample(elements=('a', 'b', 'c', 'd', 'e', 'f'))
        ,'batched':fake.random_sample(elements=('Yes', 'No', 'N/A'), length=1)[0]
        ,'loc_1':{
            'x_offset':fake.pydecimal(left_digits=2, right_digits=2, min_value=-15, max_value=15)
            ,'y_offset':fake.pydecimal(left_digits=1, right_digits=6, min_value=-1, max_value=1)
            ,'z_offset':fake.pyint(min_value=2500, max_value=5000)
        }
        ,'loc_2':{
            'x_offset':fake.pydecimal(left_digits=2, right_digits=2, min_value=-15, max_value=15)
            ,'y_offset':fake.pydecimal(left_digits=1, right_digits=6, min_value=-1, max_value=1)
            ,'z_offset':fake.pyint(min_value=2500, max_value=5000)
        }
    }
    return measurement_record
```

Repeatedly calling this function generates new records with random data that can be collected in a list up to a desired size.


```python
records_cnt = 5

measurement_record = None
measurement_list=[]

for _ in range(records_cnt):
    measurement_record = generate_measurement_record()
    measurement_list.append(measurement_record) # List of nested dictionaries
```

## Convert Dataset to XML

Next we'll need a function that will handle converting the records stored as dictionaries to xml. Then apply the function to each record in the list.  


```python
import xml.etree.ElementTree as ET

def dict_to_xml(d, r=None):
    file_id = str(uuid.uuid4().hex)
    if r is None:
        r = ET.Element('DataFile')
        r.set('id', file_id)
    if isinstance(d, dict):
        for k, v in d.items():
            s = ET.SubElement(r, k)
            dict_to_xml(v, s)
    elif isinstance(d, tuple) or isinstance(d, list):
        val = '/'.join(str(v) for v in d)
        r.text = val
    elif isinstance(d, str):
        r.text = d
    else:
        r.text = str(d)
    return r
```


```python
# Convert each record
xml_dataset = ET.Element('DataFiles')
for rcd in measurement_list:
    file_id = str(uuid.uuid4().hex)
    child = ET.SubElement(xml_dataset,'DataFile')
    child.set('id', file_id)
    
    # Convert to xml
    element= dict_to_xml(rcd,child)
```

The resulting xml file can be viewed with:


```python
from xml.dom import minidom

xml= ET.tostring(xml_dataset, encoding='unicode', method='xml')
xml= minidom.parseString(xml)
xml= xml.toprettyxml(indent='  ')

print(xml)
```

    <?xml version="1.0" ?>
    <DataFiles>
      <DataFile id="33c768494e484df9b954c4c7bae2ce68">
        <machine_id>Machine_10</machine_id>
        <test_id>3c0c95f773bf426585a3a68642d2d41a</test_id>
        <technician>Brett Kerr</technician>
        <test_routine>c/f/a/b</test_routine>
        <batched>Yes</batched>
        <loc_1>
          <x_offset>8.63</x_offset>
          <y_offset>0.39661</y_offset>
          <z_offset>3736</z_offset>
        </loc_1>
        <loc_2>
          <x_offset>-4.94</x_offset>
          <y_offset>0.964363</y_offset>
          <z_offset>3182</z_offset>
        </loc_2>
      </DataFile>
    </DataFiles>
    


## Convert Dataset to Pandas DataFrame

Pandas can directly create a DataFrame from a dictionary if the dictionary is not nested. So, the first step of conversion is to create a function to flatten the measurement dictionary structure: 


```python
import collections.abc

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
```

Next, create a new list of the flattened records: 


```python
measurement_flat_list= []

for rcd in measurement_list:
    measurement_flat_list.append(flatten(rcd)) # List of single depth dictionaries
```

Finally, convertthe list to a dataframe:


```python
measurement_df = pd.DataFrame(measurement_flat_list)
measurement_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>machine_id</th>
      <th>test_id</th>
      <th>technician</th>
      <th>test_routine</th>
      <th>batched</th>
      <th>loc_1_x_offset</th>
      <th>loc_1_y_offset</th>
      <th>loc_1_z_offset</th>
      <th>loc_2_x_offset</th>
      <th>loc_2_y_offset</th>
      <th>loc_2_z_offset</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Machine_02</td>
      <td>ffbb9f35d5484deebab0598926194203</td>
      <td>Stephanie Leblanc</td>
      <td>[f, d, c, e, a]</td>
      <td>Yes</td>
      <td>14.86</td>
      <td>0.607854</td>
      <td>3627</td>
      <td>0.63</td>
      <td>0.86374</td>
      <td>3828</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Machine_20</td>
      <td>fb824a88e0f145169b411a2180c5671c</td>
      <td>Kevin Rogers</td>
      <td>[b, a]</td>
      <td>N/A</td>
      <td>-6.14</td>
      <td>0.390133</td>
      <td>3198</td>
      <td>-4.54</td>
      <td>0.105494</td>
      <td>3099</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Machine_23</td>
      <td>25d73f925ba14df5a09a11ef8fb3a68d</td>
      <td>Robert Walters</td>
      <td>[e, a, f, d, c]</td>
      <td>N/A</td>
      <td>12.73</td>
      <td>0.410212</td>
      <td>2874</td>
      <td>-3.14</td>
      <td>0.634917</td>
      <td>2588</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Machine_07</td>
      <td>a3fb30a0fe8f4000aa72eb182230d236</td>
      <td>Cathy Martinez</td>
      <td>[f, a]</td>
      <td>N/A</td>
      <td>-14.69</td>
      <td>0.650746</td>
      <td>2915</td>
      <td>12.33</td>
      <td>0.231556</td>
      <td>2794</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Machine_21</td>
      <td>02a27172e035464fbdf680c476312b03</td>
      <td>Jeffrey Brown</td>
      <td>[a, e, f, c]</td>
      <td>No</td>
      <td>-8.33</td>
      <td>0.94833</td>
      <td>4426</td>
      <td>12.72</td>
      <td>0.731588</td>
      <td>3333</td>
    </tr>
  </tbody>
</table>
</div>



## Save Dataset Files
- XML
- CSV
- Parquet


```python
# xml
destPath = 'sample_lab_measurement.xml'
# Convert to string
xml_str= ET.tostring(xml_dataset, encoding='unicode', method='xml')

# Pretty print string 
xml_str= minidom.parseString(xml_str)
xml_str= xml_str.toprettyxml(indent='  ')

# Write file
with open(destPath, 'w') as f:  # Write in file as utf-8
    f.write(xml_str)
```


```python
# csv
destPath = 'sample_lab_measurement.csv'
measurement_df.to_csv(destPath, index = False, header=True)
```


```python
# parquet
destPath = 'sample_lab_measurement.parquet'
measurement_df.to_parquet(destPath, index = False)
```
