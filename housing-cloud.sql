# DROP TABLE amenities, customers, hotels, payments, reservations, room_amenities, rooms, room_types, staff;

CREATE TABLE Hotels (
    hotel_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE Room_Types (
    room_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE Rooms (
    room_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    hotel_id CHAR(36) NOT NULL DEFAULT (UUID()),
    room_type_id INT NOT NULL,
    room_number INT NOT NULL,
    floor INT,
    is_available BOOLEAN DEFAULT TRUE,
    rate DECIMAL(7, 2) NOT NULL,
    UNIQUE (hotel_id, floor, room_number),
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id),
    FOREIGN KEY (room_type_id) REFERENCES Room_Types(room_type_id)
);

CREATE TABLE Customers (
    customer_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(20)
);

CREATE TABLE Reservations (
    reservation_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    room_id CHAR(36) DEFAULT (UUID()) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('booked', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);

CREATE TABLE Payments (
    payment_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    amount DECIMAL(7, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('credit_card', 'debit_card', 'cash', 'online'))
);

CREATE TABLE CustomerReservationRelationship (
        customer_id CHAR(36) DEFAULT (UUID()) NOT NULL,
        payment_id CHAR(36) DEFAULT (UUID()) NOT NULL,
        reservation_id CHAR(36) DEFAULT (UUID()) NOT NULL,
        PRIMARY KEY (customer_id, payment_id, reservation_id),
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (payment_id) REFERENCES Payments(payment_id),
        FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id)
);



CREATE TABLE Staff (
    staff_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    hotel_id CHAR(36) DEFAULT (UUID()) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    position VARCHAR(100),
    hire_date DATE,
    FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id)
);

CREATE TABLE Amenities (
    amenity_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE Room_Amenities (
    room_id CHAR(36) DEFAULT (UUID()) NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (room_id, amenity_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
    FOREIGN KEY (amenity_id) REFERENCES Amenities(amenity_id)
);

