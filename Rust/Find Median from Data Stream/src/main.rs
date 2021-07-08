use std::collections::BinaryHeap;
use std::cmp::Reverse;

struct MedianFinder {
    maxheap_size: i32,
    minheap_size: i32,
    maxheap: BinaryHeap<i32>,
    minheap: BinaryHeap<Reverse<i32>>
}

impl MedianFinder {

    fn new() -> Self {
        MedianFinder{
            maxheap_size: 0,
            minheap_size: 0,
            maxheap: BinaryHeap::new(),
            minheap: BinaryHeap::new()
        }
    }

    fn add_num(&mut self, num: i32) {
        match self.minheap.peek(){
            None => {
                self.minheap.push(Reverse(num));
                self.minheap_size = self.minheap_size+1;
            }
            _ => {
                if num > self.minheap.peek().unwrap().0{
                    self.minheap.push(Reverse(num));
                    self.minheap_size = self.minheap_size+1;
                    //Balancing
                    if self.minheap_size > self.maxheap_size {
                        let temp = self.minheap.pop().unwrap_or_default().0;
                        self.minheap_size = self.minheap_size-1;

                        self.maxheap.push(temp);
                        self.maxheap_size = self.maxheap_size+1;
                    }
                } else {
                    self.maxheap.push(num);
                    self.maxheap_size = self.maxheap_size+1;
                    //Balancing
                    if self.maxheap_size > self.minheap_size {
                        let temp = self.maxheap.pop().unwrap_or_default();
                        self.minheap.push(Reverse(temp));

                        self.minheap_size = self.minheap_size+1;
                        self.maxheap_size = self.maxheap_size-1;
                    }
                }
            }
        }
    }

    fn find_median(&self) -> f64 {
        return match self.minheap_size - self.maxheap_size {
            x if x < 0 => self.maxheap.peek().unwrap().clone() as f64,
            x if x > 0 => self.minheap.peek().unwrap().clone().0 as f64,
            _ => (self.maxheap.peek().unwrap().clone() as f64 + self.minheap.peek().unwrap().clone().0 as f64) / 2f64,
        }
    }
}

/**
 * Your MedianFinder object will be instantiated and called as such:
 * let obj = MedianFinder::new();
 * obj.add_num(num);
 * let ret_2: f64 = obj.find_median();
 */

fn main() {
    let mut median_finder = MedianFinder::new();
    median_finder.add_num(1);    // arr = [1]
    println!("{}", median_finder.find_median()); // return 1
    median_finder.add_num(2);    // arr = [1,2]
    println!("{}", median_finder.find_median()); // return 1
    median_finder.add_num(3);    // arr = [1,2,3]
    println!("{}", median_finder.find_median()); // return 1
    median_finder.add_num(4);    // arr = [1,2,3,4]
    println!("{}", median_finder.find_median()); // return 1

}