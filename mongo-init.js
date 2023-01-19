db.createUser(
    {
        user: "bosco",
        pwd: " MongoExpress2019!",
        roles: [
            {
                role: "readWrite",
                db: "bhub_project"
            }
        ]
    }
);
