use serde::{Deserialize, Serialize};
use std::cmp::{max, min};
use std::ops::Range;

#[derive(Serialize, Deserialize, Debug)]
pub struct Page {
    label: String,
    number: i64,
    color: String,
}

pub fn list_pages_for(n: i64, count: i64, per_page: i64) -> Vec<Page> {
    let remaining_pages = get_remaining_pages(count, per_page);
    let delta = 10;
    let start = max(n - delta, 1);
    let end = n + min(delta, remaining_pages);
    let range = Range { start, end };
    range
        .into_iter()
        .map(|number| {
            let mut label = format!("{}", number).to_string();
            if number == start {
                label = "«".to_string();
            } else if number == end - 1 {
                label = "»".to_string();
            }
            let mut color = "".to_string();
            if number == n {
                color = "w3-green".to_string();
            }
            Page {
                label,
                number,
                color,
            }
        })
        .collect::<Vec<Page>>()
}

pub fn get_remaining_pages(count: i64, per_page: i64) -> i64 {
    let mut remaining_pages = count / per_page;
    if count % per_page != 0 {
        remaining_pages += 1;
    }
    remaining_pages
}
