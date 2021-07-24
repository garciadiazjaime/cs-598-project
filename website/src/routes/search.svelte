<script>
  import Loader from '../components/loader.svelte'

  let loading = false
  let keyword = ''
  const url = 'https://s9hjltedbi.execute-api.us-east-1.amazonaws.com/prod/picture/search'

  async function searchImage() {
    let response
    try {
      response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': 'process.apikey',
          'search-key': keyword,
        },
      });
    } catch(err) {
      return alert('Sorry, did not work this time :( try again later')
    }

    const data = response.json();

    console.log('data', data)
  }

  async function searchHandler(event) {
    if (!keyword) {
      return alert('please type in a keyword, eg. pizza')
    }

    loading = true

    await searchImage()

    loading = false
  }
</script>
<style>
  input {
    font-size: 32px;
    height: 56px;
  }

  button {
    background-color: white;
    font-size: 32px;
    border: 1px solid #ff3e00;
    padding: 12px 24px;
    border-radius: 6px;
  }
  button:hover {
    cursor: pointer;
  }
</style>
<div>
  <input type="text" bind:value={keyword}>
  <button on:click={searchHandler}>search</button>

  <Loader show={loading} />
</div>
