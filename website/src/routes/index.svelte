<script>
	import { onMount } from 'svelte';
	import Loader from '../components/loader.svelte'

	let showLabel = false
	let isFood = false
	let label = ''
	let nutrients = {}
	let isVideoOn = false
	let isMounted = false
	let loading = false

	const FOOD_API_URL = 'https://api.edamam.com/api/food-database/parser\?nutrition-type\=logging\&app_id\=07d50733\&app_key\=80fcb49b500737827a9a23f7049653b9\&ingr\='
	const UPLOAD_IMAGE_URL = 'https://xr02n7gto4.execute-api.us-west-2.amazonaws.com/default/upload-image'
	const GET_LABELS_URL = 'https://o0xm4e5shg.execute-api.us-west-2.amazonaws.com/default/get-image-labels'

	onMount(async () => {
		const video = document.getElementById('video');

		if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true })
			video.srcObject = stream
			video.play();
			isVideoOn = true
		}

		isMounted = true
	});

	function takeSnap() {
		console.log('taking snap...')
		showLabel = false
		isFood = false

		const canvas = document.getElementById('canvas');
		const context = canvas.getContext('2d');
		const video = document.getElementById('video');
		context.drawImage(video, 0, 0, 640, 480);
	}

	async function uploadImage() {
		console.log('uploading image...')
		const imageBase64 = document.getElementById('canvas').toDataURL("image/png");
		const data = {
			imageBase64
		}

		const result = await fetch(UPLOAD_IMAGE_URL, {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json'
			}
		})

		await result.json()
	}

	async function getLabels() {
		console.log('getting labels...')
		const result = await fetch(GET_LABELS_URL, {
			method: 'POST',
			body: null,
			headers: {
				'Content-Type': 'application/json'
			}
		})

		const response = await result.json()

		return response
	}

	function isFoodLabelFound(response) {
		return response && Array.isArray(response.Labels) && response.Labels.find(({ Name, Confidence }) => Name === 'Food' && Confidence > 50)
	}

	async function getNutritionalFacts(response) {
		const instance = response.Labels.find(({Instances}) => Array.isArray(Instances) && Instances.length)
		console.log({ instance })

		if (!isFood || !instance.Name) {
			return null
		}

		const option = instance.Name //'pizza'
		console.log({ option })

		const result = await fetch(`${FOOD_API_URL}${option}`)

		const foodAPIResponse = await result.json()
		console.log({ foodAPIResponse })

		if (!foodAPIResponse || !Array.isArray(foodAPIResponse.parsed) || !foodAPIResponse.parsed.length || !foodAPIResponse.parsed[0].food) {
			return null
		}

		const { food } = foodAPIResponse.parsed[0]
		
		return food
	}

	async function clickHandler() {
		loading = true

		takeSnap()

		await uploadImage()

		const labels = await getLabels()
		isFood = isFoodLabelFound(labels)
		showLabel = true

		const nutritionalFacts = await getNutritionalFacts(labels)
		if (nutritionalFacts) {
			label = nutritionalFacts.label
			nutrients = nutritionalFacts.nutrients
		}

		loading = false
	}
</script>

<style>
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

<svelte:head>
	<title>Project</title>
</svelte:head>

<h1>To eat 😇 or not to eat 😈</h1>
<video id="video" width="640" height="480" autoplay></video>

{#if isVideoOn}
	<p>
		<button id="snap" on:click={clickHandler}>Get nutritional facts 🧞</button>
	</p>

	<Loader show={loading} />

	<canvas id="canvas" width="640" height="480"></canvas>

	{#if showLabel}
		{#if isFood} 
			<h1>It's Food, yummi!</h1>
			<h2>{label}</h2>
			<p>
				For each 100G <br /><br />
				Energy: {nutrients.ENERC_KCAL}kcal <br />
				Protein: {nutrients.PROCNT}g <br />
				Fat: {nutrients.FAT}g <br />
				Carbs: {nutrients.CHOCDF}g <br />
			</p>
			<p>
				<a href="https://www.edamam.com/" target="_blank">Reference</a>
			</p>
		{:else}
			<h1>Not food :(</h1>
			
		{/if}
	{/if}
{:else if isMounted}
	<h3>Sorry, the camara is not working</h3>
{/if}

