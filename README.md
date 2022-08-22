## About the Project

After reading the book 'Architecture Patterns with Python', by Harry J.W. Percival and Bob Gregory, I wanted to get a better understanding of the philosophy of: DDD, event driven architecture, microservices, and test driven development. This repository contains code that I tried to built in line with this book.

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

### Run tests
```
make test_unit
make test_integration
```

