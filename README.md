# README

## FIRST
[Read the challenge description](https://www.hackerrank.com/challenges/cube-summation?h_r=internal-search)
This document explains how to get the application up and running, as well as how to use the API.

### Dependencies

Before starting the app, you need to make sure these dependencies are installed:
  
  * [PyMongo](https://api.mongodb.org/python/current/): Python MongoDB client.
  * [Flask](http://flask.pocoo.org/): Web micro framework for Python.
  * [Nose](https://nose.readthedocs.org/en/latest/): Test tool.
  
    **The Python version used is 3.5**
    
To install each dependency, execute the following commands in a terminal:

```
pip install pymongo
pip install flask
pip install nose
```

**NOTE:** If you have both Python 2 and 3 in your machine, use **pip3** instead

Or, better, run:

```
sudo bash dependencies.sh
```

### How to execute?

```
python application.py
```

**NOTE:** If you have both Python 2 and 3 in your machine, use **python3** instead

### API

#### Create cube:

Request URI:

```
POST /cubes
```

Request body:
```
{
    "dimension": int
}
```

**dimension** must be between 1 and 100.

Example:

```
# Request:
POST /cubes

# Body:
{"dimension": 10}

# Response:
{
    "message": "Cube created successfully",
    "data": "575cf0a57d09db2bf185dea9"
}
```
______

#### Update cube:

Request URI:

```
PUT /cubes/<cube_id>
```

Request body:
```
{
    "x": int,
    "y": int,
    "z": int,
    "value": int
}
```

**x, y, z** must be between 1 and N, where N is the cube's dimension.

Example:

```
# Request:
PUT /cubes/575cf0a57d09db2bf185dea9

# Body:
{"x": 1, "y": 2, "z": 3, "value": 42}

# Response:
{
    "message": "Cube successfully updated."
}
```
______

#### List cubes:

Request URI:

```
GET /cubes
```


Example:

```
# Request:
GET /cubes

# Response:
{
    "data": [
        {
            "_id": "575cf0a57d09db2bf185dea9",
            "cube": {
                "1": {
                    "2": {
                        "3": 42
                    }
                }
            },
            "dimension": 10
        }
    ],
    "message": "Cubes retrieved successfully."
}
```

______

#### Get single cube:

Request URI:

```
GET /cubes/<cube_id>[?x1=int[&x2=int[&y1=int[&y2=int[&z1=int[&z2=int]]]]]]
```

**Query parameters:**:
    
   * x1, y1, z1: Lower bounds of the X, Y and Z dimensions, respectively.
   * x2, y2, z2: Upper bounds of the X, Y and Z dimensions, respectively.
    
**x1, y1, z1, x2, y2, z2** must be within the cube's boundaries and must satisfy:
   
   * x1 <= x2
   * y1 <= y2
   * z1 <= z2
   
**NOTE: These parameters are optional. If none is provided, then the cube is returned as it is. On the other hand, if at least one is given, then the missing ones defaults to 1 in the case of the lower limits (x1, y1 and z1) or to N in the case of the upper limits (x2, y2 and z2) (Remember: N is the dimension of the cube). Finally, the sum of the elements within those limits is performed.**


Example:

```
# Request:
GET /cubes/575cf0a57d09db2bf185dea9

# Response:
{
    "data": {
        "_id": "575cf0a57d09db2bf185dea9",
        "cube": {
            "1": {
                "2": {
                    "3": 42
                }
            }
        },
        "dimension": 10
    },
    "message": "Cube retrieved successfully"
}
```

Example with some query parameters:

```
# Request:
GET /cubes/575cf0a57d09db2bf185dea9?x1=3&z2=9

# Response:
{
    "data": {
        "_id": "575cf0a57d09db2bf185dea9",
        "cube": {
            "1": {
                "2": {
                    "3": 42
                }
            }
        },
        "dimension": 10,
        "params": {
            "x1": 3,
            "x2": 10,
            "y1": 1,
            "y2": 10,
            "z1": 1,
            "z2": 9
        },
        "result": 0
    },
    "message": "Cube retrieved successfully"
}
```

Example with all query parameters:

```
# Request:
GET /cubes/575cf0a57d09db2bf185dea9?x1=1&x2=8&y1=2&y2=4&z1=1&z2=9

# Response:
{
    "data": {
        "_id": "575cf0a57d09db2bf185dea9",
        "cube": {
            "1": {
                "2": {
                    "3": 42
                }
            }
        },
        "dimension": 10,
        "params": {
            "x1": 1,
            "x2": 8,
            "y1": 2,
            "y2": 4,
            "z1": 1,
            "z2": 9
        },
        "result": 42
    },
    "message": "Cube retrieved successfully"
}
```

______

#### Delete single cube:

Request URI:

```
DELETE /cubes/<cube_id>
```


Example:

```
# Request:
DELETE /cubes/575cf0a57d09db2bf185dea9

# Response:
{
    "message": "Cube successfully removed"
}
```

______

#### Delete all cubes:

Request URI:

```
DELETE /cubes
```


Example:

```
# Request:
DELETE /cubes

# Response:
{
    "message": "42 cubes were removed."
}
```
