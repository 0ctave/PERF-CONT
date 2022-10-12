ports = {
    'movie':{
        'rest':'3001',
        'grpc':'3101',
        'graphql':'3201',
    },
}

paths = {
    'rest':{
        'url':'/movies/',
        'method':'GET'
    },
    'graphql':{
        'url':'/graphql',
        'method':'POST'
    }
}