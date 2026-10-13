import {z} from 'zod';
export const sensorSchema=z.object({type:z.enum(['L','M','H']),air:z.number().finite().min(250).max(400),process:z.number().finite().min(250).max(450),speed:z.number().finite().min(100).max(6000),torque:z.number().finite().min(1).max(150),wear:z.number().finite().min(0).max(500)}).strict();
