extern crate mongodb;

use mongodb::coll::Collection;
use mongodb::db::ThreadedDatabase;
use mongodb::error::Error;
use mongodb::{Client, ThreadedClient};

pub fn get_collection() -> Result<Collection, Error> {
    let client = Client::connect("localhost", 27017)?;
    Ok(client.db("model").collection("model"))
}
