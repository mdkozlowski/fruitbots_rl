<template>
  <div class="home">
	<h3>Running Environments</h3>
	<ol>
		<li v-for="(env, index) in environments" :key="index">{{env}}</li>
	</ol>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  data: function() {
	return {
		environments: []
	}
  },
  mounted: function() {
		this.getEnvironments()
  },
  methods: {
	getEnvironments: function() {
		this.axios.get('http://localhost:8721/get_environments').then(response => {
			this.environments = response.data
		})
	}
  }
}
</script>

<style lang="scss" scoped>
.home {
	list-style: none;
}
</style>
