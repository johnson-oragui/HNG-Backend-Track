const fetchClientWeather = async (lat, lng) => {
    const API_KEY = process.env.API_KEY;
    console.log('API_KEY: ', API_KEY);

    const URL = `http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${API_KEY}&units=metric`;

    try {
        const res = await fetch(URL);
        const data = await res.json();
        // console.log('data: ', data);
        const { name, main } = data;
        return { cityName: name, temperature: main.temp };
    } catch (err) {
        console.error(`Error fetching weather data: ${err.message}`);
        return { cityName: false, temperature: false };
    }
};

module.exports = fetchClientWeather;
