import { FC, useState, useEffect } from "react";

interface Props {
    className: string;
    photo: string;
    altPhoto: string;
}
 
const Img: FC<Props> = ({className, photo, altPhoto}) => {

    const [imgSrc, setImgSrc] = useState(photo);


    return (
        <>
            <img
            className={className} 
            src={imgSrc}
            onError={() => setImgSrc(altPhoto)}
            />
        </>
    )
}
 
export default Img;