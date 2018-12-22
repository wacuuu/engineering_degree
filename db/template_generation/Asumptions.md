### Layout

```json
{
	"type": "typr",
	"production_date": "DATE",
	"id": "ID",
	"parameters": {
		"key" : {"subkey": "VALUE"}
	}
}
```

Where parameters dict has various number of keys specified in invoke arg, and each key has random number of subkeys between 1 and 20

### DB table


| TYPE | DATE | ID | PARAMETERS |
|------|------|----|------------|
|  1   |   2  |  3 |      4     |


1. one of few well known strings; for example headphones, mixer, cable, guitar
2. date of production
3. 512 character hash defining product id
4. parameters list

 Each type describes a group of products, so there  will be multiple various entries from the same template. Generator script is meant to be run once.