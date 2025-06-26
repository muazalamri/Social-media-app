/* globals Chart:false, feather:false */
//flower
(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  
  fetch('/ren')
    .then(response => response.json())
    .then(response => {
      const labels = response['labels']
      const data = response['posts']
      
      // Create chart AFTER data is fetched
      const myChart = new Chart(ctx, response)
    })
    .catch(error => {
      console.error('Error fetching data:', error)
      alert('Failed to load chart data. Please try again later.')
    })
})()
//interaction
(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  
  fetch('/dashapi')
    .then(response => response.json())
    .then(response => {
      const labels = response['labels']
      const data = response['posts']
      
      // Create chart AFTER data is fetched
      const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      })
    })
    .catch(error => {
      console.error('Error fetching data:', error)
      alert('Failed to load chart data. Please try again later.')
    })
})()
//content improve
(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  
  fetch('/dashapi')
    .then(response => response.json())
    .then(response => {
      const labels = response['labels']
      const data = response['posts']
      
      // Create chart AFTER data is fetched
      const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      })
    })
    .catch(error => {
      console.error('Error fetching data:', error)
      alert('Failed to load chart data. Please try again later.')
    })
})()
//BLOG
(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  
  fetch('/dashapi')
    .then(response => response.json())
    .then(response => {
      const labels = response['labels']
      const data = response['posts']
      
      // Create chart AFTER data is fetched
      const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      })
    })
    .catch(error => {
      console.error('Error fetching data:', error)
      alert('Failed to load chart data. Please try again later.')
    })
})()
//BLOG
(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  
  fetch('/dashapi')
    .then(response => response.json())
    .then(response => {
      const labels = response['labels']
      const data = response['posts']
      
      // Create chart AFTER data is fetched
      const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      })
    })
    .catch(error => {
      console.error('Error fetching data:', error)
      alert('Failed to load chart data. Please try again later.')
    })
})()