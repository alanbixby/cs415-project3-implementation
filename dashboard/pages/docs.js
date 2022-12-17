import { useRouter } from "next/router";

export default function docs() {
  const router = useRouter()

  if (typeof window !== 'undefined') {
    if (window.location.host.includes('localhost')) {
      router.replace('http://localhost:3000/docs');
    } else {
      router.replace('https://api.ds.bxb.gg/docs');
    }
  }
  return <div>redirecting</div>
}