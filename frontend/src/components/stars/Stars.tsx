import { FC } from "react";
import { FaStar } from "react-icons/fa"; // Используем Font Awesome звёзды

interface StarsProps {
  rating: number;
  className: string;
}

const Stars: FC<StarsProps> = ({ rating, className }) => {
  return (
    <div style={{ display: "flex", gap: "4px" }} className={className}>
      {[1, 2, 3, 4, 5].map((num) => (
        <FaStar
          key={num}
          color={num <= rating ? "#008000" : "#D3D3D3"}
        />
      ))}
    </div>
  );
};

export default Stars;