rs.initiate(
	{
		_id:"myShard_1",
		members:[
			{_id:1,host:"192.168.0.51:27018",priority:2},
			{_id:2,host:"192.168.0.52:27018"},
			{_id:3,host:"192.168.0.53:27018"}
		]
	}
)