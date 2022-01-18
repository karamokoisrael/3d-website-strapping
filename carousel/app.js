const app = Vue.createApp({
    data() {
      return {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@gmail.com',
        gender: 'male',
        picture: 'https://randomuser.me/api/portraits/men/10.jpg',
        }
      },
    
      methods: {
        
        async getUser(){
          try {
            const res = await fetch("https://randomuser.me/api")
            const resJson = await res.json()
            const results = resJson.results[0];
            this.firstName = results.name.first,
            this.lastName = results.name.last,
            this.email = results.email,
            this.gender = results.gender,
            this.picture = results.picture.large
          } catch (error) {
            console.log(error);
            this.firstName = 'John',
            this.lastName = 'Doe',
            this.email = 'john@gmail.com',
            this.gender = 'male',
            this.picture = 'https://randomuser.me/api/portraits/men/10.jpg'
          }
    
    
        }
      }
    })
    
    
    app.mount('#app')