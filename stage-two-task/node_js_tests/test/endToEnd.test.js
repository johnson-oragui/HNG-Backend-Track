const request = require('supertest');

const BASE_URL = 'http://localhost:5000';

describe('End to End api tests', () => {
    it('should register a user and fetch user data', async () => {
        const registerPayload = {
            firstName: "Ben",
            lastName: "Dennis",
            email: "Ben7@gmail.com",
            password: "Ben",
            phone: "1234567890",
        };

        // perform registration
        const registerResponse = await request(`${BASE_URL}`)
            .post('/api/auth/register')
            .send(registerPayload)
            .expect(201);

        console.log(registerResponse.body);
        expect(registerResponse.body.status).toBe('success').toBe('Registration successful');
        expect(registerResponse.body.data.user.firstName).toBe(registerPayload.firstName);
        expect(registerResponse.body.data.user.lastName).toBe(registerPayload.lastName);
        expect(registerResponse.body.data.user.email).toBe(registerPayload.email);
        expect(registerResponse.body.data.user.phone).toBe(registerPayload.phone);
        expect(registerResponse.body.data.accessToken).not.toBeNull();
    });

    it('should validate error messages in registering a user', async () => {
        const registerPayload = {
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            phone: "",
        };

        const errorPayload = [
            { firstName: '', message: 'firstName must not be empty' },
            { lastName: '', message: 'lastName must not be empty' },
            { email: '', message: 'An email address must have an @-sign.' },
            { password: '', message: 'password must not be empty' },
        ];

        // perform registration
        const registerResponse = await request(`${BASE_URL}`)
            .post('/api/auth/register')
            .send(registerPayload)
            .expect(422);

        console.log(registerResponse.body);
        expect(registerResponse.body.error[0]).toStrictEqual(errorPayload[0]);
        expect(registerResponse.body.error[1]).toStrictEqual(errorPayload[1]);
        expect(registerResponse.body.error[3]).toStrictEqual(errorPayload[3]);
        expect(registerResponse.body.error[2]).toStrictEqual(errorPayload[2]);
    });

    it('should validate error message in registering a user', async () => {
        const registerPayload = {
            nothin: ''
        };

        const errorPayload = {
            status: "Bad request",
            message: "Registration unsuccessful",
            statusCode: 400
        }

        // perform registration
        const registerResponse = await request(`${BASE_URL}`)
            .post('/api/auth/register')
            .send(registerPayload)
            .expect(400);

        console.log(registerResponse.body);
        expect(registerResponse.body).toStrictEqual(errorPayload);
    });

    it('should login a user after registration', async () => {
        const loginPayload = {
            email: "Ben2@gmail.com",
            password: "Ben"
        };

        const loginResponse = await request(BASE_URL)
            .post('/api/auth/login')
            .send(loginPayload)
            .expect(200)

        consolelog(loginResponse.body);
        expect(loginResponse.body.status).toStrictEqual('success');
        expect(loginResponse.body.message).toStrictEqual("Login successful");
        expect(loginResponse.body.data.accessToken).not.toBeNull();
        expect(loginResponse.body.data.user.userId).not.toBeNull();
        expect(loginResponse.body.data.user.firstName).toStrictEqual('Ben');
        expect(loginResponse.body.data.user.lastName).toStrictEqual('Dennis');
        expect(loginResponse.body.data.user.email).toStrictEqual('Ben2@gmail.com');
        expect(loginResponse.body.data.user.phone).toStrictEqual('1234567890');
    });
});
