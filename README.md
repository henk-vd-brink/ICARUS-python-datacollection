## About the Project

After reading the book 'Architecture Patterns with Python', by Harry J.W. Percival and Bob Gregory, I wanted to get a better understanding of the philosophy of DDD, event driven architecture and test driven development. This repository contains code that is built in line with this book, the great thing about the architecture discussed in this book, is that the business logic is completely decoupled from the implementation. The domain does not care about how- and where things are stored.

## Getting Started
### Prerequisites
- Docker

### Installation
```
git clone https://github.com/henk-vd-brink/ICARUS-python-datacollection.git
cd ICARUS-python-datacollection
```

### Build
```
docker-compose -f docker-compose.build.yaml build
```

### Run
```
docker-compose -f docker-compose.dev.yaml up
```

