rs.initiate(
  {
    _id: "configRS",
    configsvr: true,
    members: [
      { _id : 0, host : "192.168.0.51:27019" },
      { _id : 1, host : "192.168.0.52:27019" },
      { _id : 2, host : "192.168.0.53:27019" }
    ]
  }
)