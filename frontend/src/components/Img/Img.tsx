import { FC, useState } from "react";

interface Props {
    className: string;
    photo?: string;
    altPhoto: string;
}
 
const Img: FC<Props> = ({className, photo, altPhoto}) => {
    
    const [imgSrc, setImgSrc] = useState(photo);
    
    
    console.log(photo);


    return (
        <>
            {imgSrc ?
            <img
            className={className} 
            src={imgSrc}
            onError={() => setImgSrc(altPhoto)}
            /> 
            :
            <img
            className={className} 
            src={altPhoto} />
            }
        </>
    )
}
 
export default Img;