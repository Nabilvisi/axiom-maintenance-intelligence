import {sensorSchema} from '@/lib/validation';
import {explain} from '@/lib/inference';
export async function POST(request:Request){
 if(Number(request.headers.get('content-length')||0)>4096)return Response.json({error:'Request too large'},{status:413});
 try{
  if(!request.body)return Response.json({error:'Request must contain valid JSON.'},{status:400});
  const reader=request.body.getReader();const chunks:Uint8Array[]=[];let size=0;
  while(true){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;if(size>4096){await reader.cancel();return Response.json({error:'Request too large'},{status:413})}chunks.push(value)}
  const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength}
  const parsed=sensorSchema.safeParse(JSON.parse(new TextDecoder().decode(bytes)));
  if(!parsed.success)return Response.json({error:'Enter valid sensor values within the supported bounds.',details:parsed.error.flatten()},{status:400});
  return Response.json(explain(parsed.data),{headers:{'Cache-Control':'no-store'}})
 }catch{return Response.json({error:'Request must contain valid JSON.'},{status:400})}
}
