export async function getConfigs(callback) {
    const resp = await fetch("/api/configs");
    callback(await resp.json());
}
